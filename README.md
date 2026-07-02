# vision-rag

FastAPI skeleton for an image RAG knowledge base system.

当前项目包含一个轻量 FastAPI 后端、内置前端页面，以及仅用于数据库层的 Docker Compose 配置。AI 逻辑、真实向量化、真实图像生成暂未实现。

## 功能概览

- FastAPI 分层结构
- 内置前端页面：上传、检索对话、生成占位交互
- Upload / Search / Generate API 占位接口
- SQLAlchemy 模型预留
- PostgreSQL 15 + pgvector Docker 数据库环境
- pgvector `vector(512)` 字段与相似度检索基础支持

## 项目结构

```text
vrag/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── db/
│   ├── vector/
│   ├── utils/
│   ├── templates/
│   └── static/
├── data/
│   └── uploads/
├── docker-compose.yml
├── init.sql
├── requirements.txt
├── .env
└── README.md
```

## 启动应用

```powershell
cd E:\Work\vrag
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

访问前端页面：

```text
http://127.0.0.1:8000/
```

后端接口：

- `GET /health`
- `POST /api/v1/upload`
- `POST /api/v1/search`
- `POST /api/v1/generate`

## 启动数据库

当前 Docker 配置只部署数据库，不部署 FastAPI 应用服务。

```powershell
cd E:\Work\vrag
docker-compose up -d
```

如果使用新版 Docker Compose，也可以执行：

```powershell
docker compose up -d
```

停止数据库：

```powershell
docker-compose down
```

如果需要同时删除数据库持久化数据：

```powershell
docker-compose down -v
```

## 数据库连接信息

`docker-compose.yml` 中默认配置：

```text
Host: 127.0.0.1
Port: 5432
Database: vision_rag
User: vision_rag
Password: vision_rag_password
```

连接命令：

```powershell
docker exec -it vision-rag-postgres psql -U vision_rag -d vision_rag
```

也可以使用本机 psql：

```powershell
psql "postgresql://vision_rag:vision_rag_password@127.0.0.1:5432/vision_rag"
```

## 验证 pgvector

进入数据库后执行：

```sql
SELECT extname, extversion
FROM pg_extension
WHERE extname = 'vector';
```

验证 `vector` 类型可用：

```sql
SELECT '[1,2,3]'::vector;
```

查看初始化表：

```sql
\d images
```

`images` 表包含：

- `id BIGSERIAL PRIMARY KEY`
- `image_url TEXT`
- `designer_id INT`
- `embedding VECTOR(512)`
- `created_at TIMESTAMP`

## 向量相似度查询示例

插入一条测试数据，示例向量使用 512 维零向量：

```sql
INSERT INTO images (image_url, designer_id, embedding)
VALUES (
    '/data/uploads/example.png',
    1,
    ('[' || array_to_string(array_fill(0.1::float8, ARRAY[512]), ',') || ']')::vector
);
```

Cosine 距离查询：

```sql
SELECT
    id,
    image_url,
    designer_id,
    embedding <=> ('[' || array_to_string(array_fill(0.1::float8, ARRAY[512]), ',') || ']')::vector AS cosine_distance
FROM images
ORDER BY embedding <=> ('[' || array_to_string(array_fill(0.1::float8, ARRAY[512]), ',') || ']')::vector
LIMIT 5;
```

L2 距离查询：

```sql
SELECT
    id,
    image_url,
    designer_id,
    embedding <-> ('[' || array_to_string(array_fill(0.1::float8, ARRAY[512]), ',') || ']')::vector AS l2_distance
FROM images
ORDER BY embedding <-> ('[' || array_to_string(array_fill(0.1::float8, ARRAY[512]), ',') || ']')::vector
LIMIT 5;
```

按设计师过滤后检索：

```sql
SELECT
    id,
    image_url,
    designer_id
FROM images
WHERE designer_id = 1
ORDER BY embedding <=> ('[' || array_to_string(array_fill(0.1::float8, ARRAY[512]), ',') || ']')::vector
LIMIT 5;
```

## Future TODO

- TODO: Add CLIP image and text embedding implementation.
- TODO: Add PostgreSQL connection management in FastAPI.
- TODO: Add vector search against persisted image embeddings.
- TODO: Add designer style metadata filtering.
- TODO: Add Stable Diffusion or another image generation backend.
