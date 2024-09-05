# Blog Website

This is a Django-based blog website that allows users to view, comment and share blog posts. It features tagging capabilities using the `django-taggit` library, an integrated sitemap, and a responsive design using Tailwind CSS.

## Features

- **Create and Manage Blog Posts**: Users can view, comment, and share blog posts. admins can create the blog posts.
- **Tagging System**: Posts can be tagged, allowing users to filter posts by tags.
- **Responsive Design**: The website is mobile-friendly with a clean, modern layout.
- **SEO Friendly**: Sitemap integration for better search engine indexing.
- **Admin Panel**: Full-featured admin panel for managing content, users, and site settings.

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Basic knowledge of Docker, Django, and PostgreSQL.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/blog-website.git
cd blog-app
```

### 2. Create/Run the container

- Terminate connections to db, drop current db, create db, load data form
```bash
docker-compose up --build
```

### 3. Optional (add data)

- Terminate connections to db, drop current db, create db, load data form file

```bash
docker exec -i blog_app-db-1 psql -U blog -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'blog' AND pid <> pg_backend_pid();" && \
docker exec -i blog_app-db-1 psql -U blog -d postgres -c "DROP DATABASE blog;" && \
docker exec -i blog_app-db-1 psql -U blog -d postgres -c "CREATE DATABASE blog;" && \
docker exec -i blog_app-db-1 psql -U blog -d blog < db.sql
```
```
