COPY (
    WITH spam_records (id, transaction_id) AS (
        SELECT
            r.id, r.transaction_id
        FROM records_metadata_version as r
            JOIN pidstore_pid
                ON pidstore_pid.object_uuid = r.id
        WHERE
            r.json IS NOT NULL AND
            r.json->>'removal_reason' ILIKE '%spam%' AND
            r.end_transaction_id IS NULL AND
            pidstore_pid.pid_type = 'recid' AND
            pidstore_pid.status = 'D' AND
            pidstore_pid.object_type = 'rec'
    )

    SELECT
        json_build_object(
            'recid', r.json->'recid',
            'title', r.json->'title',
            'description', r.json->'description',
            -- 'files', r.json->'recid',
            -- 'license', r.json->'license',
            -- 'access_right', r.json->'access_right',
            -- 'creators', r.json->'creators',
            -- 'communities', r.json->'communities',
            -- 'publication_date', r.json->'publication_date',
            -- 'keywords', r.json->'keywords',
            -- 'subjects', r.json->'subjects',
            -- 'notes', r.json->'notes',
            -- 'resource_type', r.json->'resource_type',
            -- 'related_identifiers', r.json->'related_identifiers',
            -- 'contributors', r.json->'contributors',
            -- 'doi', r.json->'doi',
            -- 'journal', r.json->'journal',
            -- 'alternate_identifiers', r.json->'alternate_identifiers',
            -- 'imprint', r.json->'imprint',
            -- 'references', r.json->'references',
            -- 'thesis', r.json->'thesis',
            -- 'meeting', r.json->'meeting',
            -- 'part_of', r.json->'part_of',
            -- 'owners', r.json->'owners',
            'spam', true
        )
    FROM records_metadata_version as r
        JOIN spam_records as s
            ON r.id = s.id AND r.end_transaction_id = s.transaction_id
) TO STDOUT;
