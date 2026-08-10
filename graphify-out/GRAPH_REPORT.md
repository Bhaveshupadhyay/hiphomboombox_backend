# Graph Report - workspace_target  (2026-08-10)

## Corpus Check
- 25 files · ~2,994 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 146 nodes · 288 edges · 9 communities (8 shown, 1 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fc679086`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FeaturedPost
- Post
- client.py
- v1/post.py
- Category
- dependency.py
- Workflow Steps
- Code Architecture & Contribution Guidelines
- hiphopboombox-backend

## God Nodes (most connected - your core abstractions)
1. `Post` - 19 edges
2. `PostRepository` - 14 edges
3. `Category` - 13 edges
4. `FeaturedPost` - 12 edges
5. `PostService` - 12 edges
6. `get_post_service()` - 11 edges
7. `CategoryRepository` - 11 edges
8. `FeaturedPostRepository` - 10 edges
9. `CategoryCreate` - 8 edges
10. `FeaturedPostCreate` - 8 edges

## Surprising Connections (you probably didn't know these)
- `create_category()` --references--> `CategoryCreate`  [EXTRACTED]
  app/api/v1/category.py → app/schemas/category.py
- `create_post()` --references--> `PostCreate`  [EXTRACTED]
  app/api/v1/post.py → app/schemas/post.py
- `get_category_repo()` --references--> `CategoryRepository`  [EXTRACTED]
  app/core/dependency.py → app/repositories/category.py
- `get_featured_repo()` --references--> `FeaturedPostRepository`  [EXTRACTED]
  app/core/dependency.py → app/repositories/featured.py
- `get_post_repo()` --references--> `PostRepository`  [EXTRACTED]
  app/core/dependency.py → app/repositories/post.py

## Import Cycles
- None detected.

## Communities (9 total, 1 thin omitted)

### Community 0 - "FeaturedPost"
Cohesion: 0.15
Nodes (14): create_featured_post(), get_featured_posts(), Get all featured posts for the desktop and mobile homepage carousel., Create a new featured post (internal or for admin use)., get_featured_service(), FeaturedPost, Base, FeaturedPostRepository (+6 more)

### Community 1 - "Post"
Cohesion: 0.17
Nodes (5): Post, Base, PostRepository, PostCreate, PostService

### Community 2 - "client.py"
Cohesion: 0.16
Nodes (16): Any, cached(), get_redis_key(), insert_redis_data(), close_connection(), close_postgres_client(), close_redis_client(), get_redis_client() (+8 more)

### Community 3 - "v1/post.py"
Cohesion: 0.14
Nodes (20): create_post(), get_post_by_id(), get_posts(), get_posts_by_category(), get_posts_by_date(), get_trending_posts(), Get homepage posts grouped by today, yesterday, and day before yesterday., Get trending posts sorted by view count descending. (+12 more)

### Community 4 - "Category"
Cohesion: 0.18
Nodes (9): Category, Base, CategoryRepository, CategoryBase, CategoryCreate, CategoryResponse, Config, BaseModel (+1 more)

### Community 5 - "dependency.py"
Cohesion: 0.26
Nodes (11): create_category(), get_categories(), Get all active categories., Create a new category (internal or for admin use)., get_postgres_client(), get_category_repo(), get_category_service(), get_db() (+3 more)

### Community 6 - "Workflow Steps"
Cohesion: 0.22
Nodes (8): PR Review Comment Resolution Guide, Principles, Step 1: Fetch PR Review Comments, Step 2: Evaluate Each Comment, Step 3: Implement & Verify Fixes, Step 4: Commit, Push & Respond on GitHub, Trigger Phrases, Workflow Steps

### Community 7 - "Code Architecture & Contribution Guidelines"
Cohesion: 0.33
Nodes (5): 1. Tech Stack & Infrastructure, 2. Layered Architecture Pattern, 3. Contribution Guidelines, Code Architecture & Contribution Guidelines, Layer Responsibilities:

## Knowledge Gaps
- **13 isolated node(s):** `Config`, `Config`, `Config`, `hiphopboombox-backend`, `1. Tech Stack & Infrastructure` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PostRepository` connect `Post` to `dependency.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `PostService` connect `Post` to `v1/post.py`, `dependency.py`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `get_post_service()` connect `v1/post.py` to `Post`, `dependency.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Post` (e.g. with `PostRepository` and `PostService`) actually correct?**
  _`Post` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Category` (e.g. with `CategoryRepository` and `CategoryService`) actually correct?**
  _`Category` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `FeaturedPost` (e.g. with `FeaturedPostRepository` and `FeaturedPostService`) actually correct?**
  _`FeaturedPost` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Config`, `Config` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._