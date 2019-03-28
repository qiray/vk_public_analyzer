# vk_public_analyzer

```sql
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER,
    from_id INTEGER,
    owner_id INTEGER,
    signer_id INTEGER,
    date INTEGER,
    marked_as_ads INTEGER,
    post_type TEXT,
    text TEXT,
    is_pinned INTEGER,
    comments_count INTEGER,
    likes_count INTEGER,
    reposts_count INTEGER,
    views_count INTEGER,
    PRIMARY KEY (id, from_id)
);

CREATE TABLE IF NOT EXISTS attachments (
    type TEXT,
    id INTEGER,
    owner_id INTEGER,
    post_id INTEGER,
    url TEXT,
    additional_info text,
    PRIMARY KEY (id, type, post_id)
);
```

## What we can

- Show common data
- Build word cloud
