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
    attachments_count INTEGER,
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

- Show statistics about likes, reposts, views, comments, ads and attachments;
- Show top posts - by likes, reposts, views, comments, attachments and text length;
- Show count of posts without texts, likes, reposts, comments and attachments;
- Show count of each known attachment types;
- Show authors info - count of posts, likes, reposts, comments, views, attachments and text length; 
- Find top words and hashtags;
- Build word cloud;
- Make output images and csv-files.

## Thanks

- Yandex Mystem;
- Some python libs.

## How you can help

- Contribute;
- Star and repost on github - [https://github.com/qiray/vk_public_analyzer](https://github.com/qiray/vk_public_analyzer);
- Tell your friends;
- Write an article;
- Use in your project;
- Donate.
