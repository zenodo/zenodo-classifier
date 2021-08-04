import datetime
import json
from collections import Counter, namedtuple
from itertools import groupby, takewhile
import gzip

from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier
from invenio_records.api import Record
from invenio_records.models import RecordMetadata
from sqlalchemy.orm import join, mapper, query


def parse_record(rec, spam=False):
    out = {}
    # Fetch files
    out["files"] = []
    if "_files" in rec and rec.get("access_right") == "open":
        for f in rec["_files"]:
            f_json = {"filename": f["key"], "filetype": f["type"], "size": f["size"]}
            out["files"].append(f_json)
    # Fetch the fixed keys
    out["recid"] = rec["recid"]  # Recid has to be there
    out["license"] = (
        rec["license"]["$ref"].split("licenses/")[1] if "license" in rec else None
    )
    keys = [
        "access_right",
        "creators",
        "title",
        "description",
        "communities",
        "publication_date",
        "keywords",
        "subjects",
        "notes",
        "resource_type",
        "related_identifiers",
        "contributors",
        "doi",
        "journal",
        "alternate_identifiers",
        "imprint",
        "references",
        "thesis",
        "meeting",
        "part_of",
        "owners",
    ]
    for key in keys:
        out[key] = rec.get(key, None)
    # Insert the spam label
    out["spam"] = spam
    return out

DUMP_TYPES = {
  '1': 'ham',
  '2': 'spam',
  '3': 'full',
}

choices = [k + ' - ' + v for k, v in DUMP_TYPES.items()]
choice = str(input("What type of dump you want? {}".format(', '.join(choices)) + '\n'))
dump_type = DUMP_TYPES.get(choice)

if not dump_type:
    raise Exception('Invalid dump type {}'.format(choice))

today = datetime.date.today().isoformat()
FILENAME = "zenodo_open_metadata_" + dump_type + '_' + today + ".jsonl.gz"

if dump_type in ('spam', 'full'):
    records_ham = (
        db.session.query(RecordMetadata)
        .join(PersistentIdentifier, PersistentIdentifier.object_uuid == RecordMetadata.id)
        .filter(
            PersistentIdentifier.pid_type == "recid",
            PersistentIdentifier.status == "R",
            PersistentIdentifier.object_type == "rec",
        )
    )

    # Write the non-spam records first
    total_ham = records_ham.count()
    with gzip.open(FILENAME, "ab") as fp:
        for idx, r in enumerate(records_ham.yield_per(1000)):
            if idx % 10000 == 0:
                print('[{}]: {} / {}'.format(datetime.datetime.now().isoformat(), idx, total_ham))
            if r.json is not None:
                rec = parse_record(Record(r.json, model=r), spam=False)
                fp.write(json.dumps(rec) + "\n")

if dump_type in ('ham', 'full'):
    records_spam = (
        db.session.query(RecordMetadata)
        .join(PersistentIdentifier, PersistentIdentifier.object_uuid == RecordMetadata.id)
        .filter(
            PersistentIdentifier.pid_type == "recid",
            PersistentIdentifier.status == "D",
            PersistentIdentifier.object_type == "rec",
        )
    )

    # Write the SPAM records
    failing_records = []
    total_spam = records_spam.count()
    with gzip.open(FILENAME, "ab") as fp:
        for idx, r in enumerate(records_spam.yield_per(1000)):
            if idx % 1000 == 0:
                print('[{}]: {} / {}'.format(datetime.datetime.now().isoformat(), idx, total_spam))
            try:
                if (
                    r.json is not None
                    and "removal_reason" in r.json
                    and "spam" in r.json["removal_reason"].lower()
                ):
                    rec = parse_record(Record(r.json, model=r).revisions[-2], spam=True)
                    fp.write(json.dumps(rec) + "\n")
            except Exception as ex:
                failing_records.append((r, ex))
