CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS images (
    id BIGSERIAL PRIMARY KEY,
    image_url TEXT NOT NULL,
    designer_id INT,
    embedding VECTOR(512),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_images_designer_id
    ON images (designer_id);

-- TODO: Tune vector index type and parameters after real data volume is known.
CREATE INDEX IF NOT EXISTS idx_images_embedding_cosine
    ON images
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
