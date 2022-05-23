COPY (
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
            'spam', false
        )
    FROM records_metadata as r
        JOIN pidstore_pid
            ON pidstore_pid.object_uuid = r.id
    WHERE
        r.json IS NOT NULL AND
        pidstore_pid.pid_type = 'recid' AND
        pidstore_pid.status = 'R' AND
        pidstore_pid.object_type = 'rec'
) TO STDOUT;
