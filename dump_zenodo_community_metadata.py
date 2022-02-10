from invenio_communities.models import Community
import gzip
import json
import datetime

filename = 'zenodo_community_metadata_{}.jsonl.gz'.format(datetime.date.today().isoformat())
with gzip.open(filename, 'wb') as fp:
    for c in Community.query.yield_per(1000):
        is_spam = (
            c.deleted_at is not None and
            c.description is not None and
            c.description.lower().startswith('--spam--')
        )
        fp.write(json.dumps({
            'id': c.id,
            'title': c.title,
            'description': c.description.replace('--SPAM--', ''),
            'curation_policy': c.curation_policy,
            'page': c.page,
            'spam': is_spam,
        }) + '\n')
