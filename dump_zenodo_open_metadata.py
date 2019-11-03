import datetime
import json
from collections import Counter, namedtuple
from itertools import groupby, takewhile

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


FILENAME = "zenodo_open_metadata_{}.txt".format(datetime.datetime.now().isoformat())

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
with open(FILENAME, "w") as fp:
    for r in records_ham.yield_per(1000):
        if r.json is not None:
            rec = parse_record(Record(r.json, model=r), spam=False)
            fp.write(json.dumps(rec) + "\n")

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
with open(FILENAME, "a") as fp:
    for r in records_spam.yield_per(1000):
        if (
            r.json is not None
            and "removal_reason" in r.json
            and "spam" in r.json["removal_reason"].lower()
        ):
            try:
                rec = parse_record(Record(r.json, model=r).revisions[-2], spam=True)
                fp.write(json.dumps(rec) + "\n")
            except:
                failing_records.append(r)
