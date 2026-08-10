# Graph Report - hiphopboombox-backend  (2026-08-09)

## Corpus Check
- 24 files · ~3,545 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 152 nodes · 295 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6cf6ca41`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FeaturedPost
- Post
- client.py
- dependency.py
- Category
- v1/category.py
- hiphopboombox-backend
- Layer Responsibilities

## God Nodes (most connected - your core abstractions)
1. `Post` - 19 edges
2. `PostRepository` - 14 edges
3. `Category` - 13 edges
4. `FeaturedPost` - 12 edges
5. `PostService` - 12 edges
6. `Layer Responsibilities` - 12 edges
7. `get_post_service()` - 11 edges
8. `CategoryRepository` - 11 edges
9. `FeaturedPostRepository` - 10 edges
10. `FastAPI Project Structure & Code Style Guide` - 9 edges

## Surprising Connections (you probably didn't know these)
- `create_category()` --references--> `CategoryCreate`  [EXTRACTED]
  app/api/v1/category.py → app/schemas/category.py
- `get_category_repo()` --references--> `CategoryRepository`  [EXTRACTED]
  app/core/dependency.py → app/repositories/category.py
- `get_featured_repo()` --references--> `FeaturedPostRepository`  [EXTRACTED]
  app/core/dependency.py → app/repositories/featured.py
- `get_post_repo()` --references--> `PostRepository`  [EXTRACTED]
  app/core/dependency.py → app/repositories/post.py
- `get_category_service()` --references--> `CategoryService`  [EXTRACTED]
  app/core/dependency.py → app/services/category.py

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "FeaturedPost"
Cohesion: 0.15
Nodes (14): create_featured_post(), get_featured_posts(), Get all featured posts for the desktop and mobile homepage carousel., Create a new featured post (internal or for admin use)., get_featured_service(), FeaturedPost, Base, FeaturedPostRepository (+6 more)

### Community 1 - "Post"
Cohesion: 0.17
Nodes (4): Post, Base, PostRepository, PostService

### Community 2 - "client.py"
Cohesion: 0.21
Nodes (13): Any, cached(), get_redis_key(), insert_redis_data(), close_connection(), close_postgres_client(), close_redis_client(), get_redis_client() (+5 more)

### Community 3 - "dependency.py"
Cohesion: 0.11
Nodes (27): create_post(), get_post_by_id(), get_posts(), get_posts_by_category(), get_posts_by_date(), get_trending_posts(), Get homepage posts grouped by today, yesterday, and day before yesterday., Get trending posts sorted by view count descending. (+19 more)

### Community 4 - "Category"
Cohesion: 0.18
Nodes (9): Category, Base, CategoryRepository, CategoryBase, CategoryCreate, CategoryResponse, Config, BaseModel (+1 more)

### Community 5 - "v1/category.py"
Cohesion: 0.25
Nodes (8): create_category(), get_categories(), Get all active categories., Create a new category (internal or for admin use)., get_category_service(), Root status check endpoint., read_root(), FastAPI

### Community 7 - "Layer Responsibilities"
Cohesion: 0.10
Nodes (20): `app/api/v1/<entity>.py` — Route Handlers, `app/api/v1/router.py` — API Router Aggregator, `app/core/client.py` — DB & Redis Clients, `app/core/config.py` — Settings, `app/core/dependency.py` — Dependency Injection, `app/core/lifespan.py` — Lifespan, `app/main.py` — App Entry Point, `app/models/<entity>.py` — SQLAlchemy Models (+12 more)

## Knowledge Gaps
- **22 isolated node(s):** `Config`, `Config`, `Config`, `hiphopboombox-backend`, `Tech Stack` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PostRepository` connect `Post` to `dependency.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `PostService` connect `Post` to `dependency.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `get_post_service()` connect `dependency.py` to `Post`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Post` (e.g. with `PostRepository` and `PostService`) actually correct?**
  _`Post` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Category` (e.g. with `CategoryRepository` and `CategoryService`) actually correct?**
  _`Category` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `FeaturedPost` (e.g. with `FeaturedPostRepository` and `FeaturedPostService`) actually correct?**
  _`FeaturedPost` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Config`, `Config` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._