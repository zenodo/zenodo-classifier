COPY (
    SELECT
        json_build_object(
            'id', id,
            'title', title,
            'description', description,
            'curation_policy', curation_policy,
            'page', page,
            'spam', false
        )
    FROM communities_community
    WHERE
        deleted_at IS NULL
) TO STDOUT;
