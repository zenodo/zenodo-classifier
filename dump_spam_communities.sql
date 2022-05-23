COPY (
    SELECT
        json_build_object(
            'id', id,
            'title', title,
            'description', replace(description, '--SPAM--', ''),
            'curation_policy', curation_policy,
            'page', page,
            'spam', true
        )
    FROM communities_community
    WHERE
        deleted_at IS NOT NULL AND
        description IS NOT NULL AND
        description ILIKE '--spam--%'
) TO STDOUT;
