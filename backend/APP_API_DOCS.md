# API Docs

FastAPI auto-generates OpenAPI:
- Swagger UI: /docs
- OpenAPI JSON: /openapi.json

Core endpoints:
- Profiles
  - POST /profiles
  - GET /profiles/{id}
  - PUT /profiles/{id}
  - DELETE /profiles/{id}
  - GET /profiles?height_category_id=&weight_category_id=
- Categories
  - GET /categories/height
  - GET /categories/weight

Use Bearer tokens for authentication in the future; current scaffold does not enforce auth.
