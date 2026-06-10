# Containerized Django 5 Blogging Platform

A professional, containerized blogging system built with **Django 5** and **PostgreSQL**. The platform features tag-based categorization, interactive post sharing, sitemap SEO optimization, and is fully orchestratable using **Docker Compose**.

## 🚀 Key Features

*   **Django 5 & PostgreSQL Backend**: Solid database relational modeling with Django's object-relational mapper (ORM).
*   **Tagging System**: Fast content categorization using the `django-taggit` package.
*   **SEO-Friendly Assets**: Integrated Django sitemaps (`sitemap.xml`) and RSS feeds (`feed.xml`) for optimal indexing by search engines.
*   **Markdown Support**: Direct editing and rendering of Markdown-formatted blog posts.
*   **Tailwind CSS UI**: Modern, fully responsive, and elegant frontend layout.
*   **Dockerized Infrastructure**: Packaged with a custom `Dockerfile` and `docker-compose.yml` for unified development and staging setups.

---

## 🛠 Tech Stack & Tools

- **Backend**: Python 3.11+, Django 5.x
- **Database**: PostgreSQL
- **Design System**: Tailwind CSS, Django Widget Tweaks
- **Containerization**: Docker, Docker Compose
- **Server Gateway**: Gunicorn

---

## 🐋 Getting Started with Docker

### Prerequisites
- Docker and Docker Compose installed on your system.

### 1. Clone & Navigate
```bash
git clone https://github.com/Josue-Tejeda/blog-app.git
cd blog-app
```

### 2. Launch the Application Container
Execute the Docker Compose command to build the Python app image and start the PostgreSQL database container:
```bash
docker-compose up --build
```
This launches:
- **Web App**: listening on `http://localhost:8000`
- **Database**: PostgreSQL listening on `localhost:5432`

### 3. Load Sample Data (Optional)
If you wish to load the pre-configured schema and dummy blog posts, execute the database recovery commands:
```bash
# Terminate other sessions and reset the blog database
docker exec -i blog_app-db-1 psql -U blog -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'blog' AND pid <> pg_backend_pid();"
docker exec -i blog_app-db-1 psql -U blog -d postgres -c "DROP DATABASE blog;"
docker exec -i blog_app-db-1 psql -U blog -d postgres -c "CREATE DATABASE blog;"

# Restore the dump file
docker exec -i blog_app-db-1 psql -U blog -d blog < db.sql
```
Once restored, log in with admin credentials to populate more posts!
