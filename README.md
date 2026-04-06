# ZorvynFinance
Finance Data Processing and Access Control. 
# Finance Dashboard API

A production-quality backend for a role-based finance management system, built with **Django REST Framework** and **PostgreSQL**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the Server](#running-the-server)
- [API Reference](#api-reference)
- [Role-Based Access Control](#role-based-access-control)
- [Optional Enhancements Implemented](#optional-enhancements-implemented)

---

### Test Credentials (Live API)

A default admin account is automatically created on deployment.
Use these credentials to log in at `/api/v1/users/auth/login/`:

| Field    | Value                        |
|----------|------------------------------|
| Email    | admin@zorvynfinance.com      |
| Username | admin                        |
| Password | Admin@1234!                  |

> **Tip:** Log in via `POST /api/v1/users/auth/login/`, copy the `access` 
> token from the response, click **Authorize** in Swagger UI, 
> and paste `Bearer <token>` to unlock all protected endpoints

## Project Overview

This backend powers a finance dashboard where different users interact with financial records based on their role. It supports:

- **JWT authentication** with token refresh and blacklisting on logout
- **Only Admin users can create Admin and Analyst user.**
- **Public registration endpoint only for Viewers.**
- **Three-tier role system**: Viewer → Analyst → Admin
- **Financial records** (income/expense) with categories, filtering, and soft-delete
- **Dashboard analytics**: summaries, category breakdowns, monthly trends
- **Rate limiting**, **pagination**, **search**, and **Swagger UI** out of the box

---

## Architecture

```
Client / Frontend
        │  HTTPS + JWT
        ▼
Django REST Framework
(Rate limiting · Swagger · JWT )
        │
        ├── users app         Auth · Roles · JWT
        ├── records app       CRUD · Filter · Soft-delete
        └── analytics app     Dashboard · Trends
                │
        Permissions & Access Control
        (IsAdmin · IsAnalyst · IsViewer)
                │
        PostgreSQL Database
        (users · financial_records · categories)
```

**Key patterns used:**

- **Custom exception handler** — every error response has a consistent `{ error: { code, message, details } }` envelope
- **Soft-delete** — financial records are never physically removed; they get `is_deleted=True` for audit trail integrity
- **Custom manager** — `SoftDeleteManager` hides deleted records automatically; views never need to filter manually

---

## Tech Stack

| Concern | Choice | Why |
|---|---|---|
| Framework | Django 5.1.4 + DRF 3.17 | Mature, batteries-included, excellent ORM |
| Database | PostgreSQL | Industry-standard for financial systems; strong decimal precision, concurrency |
| Auth | JWT (SimpleJWT) | Stateless, scalable; refresh + blacklist on logout |
| API Docs | drf-spectacular (Swagger) | Auto-generated from code, always in sync, interactive UI |
| Filtering | django-filter | Declarative, composable filter sets |
| Rate Limiting | DRF throttling | Per-scope limits for auth vs regular endpoints |

---
````
## Project Structure

````
## Project Structure
ZorvynFinance/                        ← GitHub repo root
├── build.sh                          ← Render build script
├── render.yaml                       ← Render infrastructure config
├── .gitignore
├── README.md
│
└── finance_dashboard/                ← Django project root
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    │
    ├── finance_dashboard/            ← Django config package
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    └── apps/
        ├── core/                     ← Shared utilities
        │   ├── models.py             ← TimeStampedModel, SoftDeleteModel
        │   ├── exceptions.py         ← Consistent error envelope
        │   ├── middleware.py         ← Request logging
        │   └── responses.py         ← success() / error() helpers
        │
        ├── users/                    ← Auth & user management
        │   ├── models.py             ← User model with roles
        │   ├── serializers.py        ← JWT, registration, user detail
        │   ├── views.py              ← Login, logout, register, profile, CRUD
        │   ├── permissions.py        ← IsAdmin, IsAnalystOrAdmin, IsAdminOrReadOnly
        │   └── urls.py
        │
        ├── records/                  ← Financial records
        │   ├── models.py             ← Category, FinancialRecord (soft-delete)
        │   ├── serializers.py
        │   ├── views.py
        │   ├── filters.py            ← Date, amount, type filters
        │   └── urls.py
        │
        └── analytics/                ← Dashboard APIs
            ├── views.py              ← Summary, trends, breakdown, recent
            └── urls.py


---

## Setup & Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip

### 1. Clone and create virtual environment

```bash
git clone <your-repo-url>
cd finance_dashboard

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

### 4. Create the PostgreSQL database

```bash
psql -U postgres
CREATE DATABASE zorvyndb;
\q
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (Admin role)

```bash
python manage.py createsuperuser
```

When prompted, enter your email, username, and password. This user will have the `ADMIN` role and full access.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | (insecure default) | Django secret key — **change in production** |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `*` | "localhost","127.0.0.1",".onrender.com", |
| `DB_NAME` | `zorvyndb` | PostgreSQL database name |
| `DB_USER` | `zorvynuser` | PostgreSQL user |
| `DB_PASSWORD` | `zorvyn123` | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |

---

## Running the Server

- **Live API (Render):** `https://zorvynfinance.onrender.com/api/v1/`
- **Swagger UI:** `https://zorvynfinance.onrender.com/api/docs/`
- **ReDoc:** `https://zorvynfinance.onrender.com/api/redoc/`
- **Django Admin:** `https://zorvynfinance.onrender.com/admin/`

### Local Development
- **API Base URL:** `http://localhost:8000/api/v1/`
- **Swagger UI:** `http://localhost:8000/api/docs/`

---

## API Reference

### Authentication — `/api/v1/auth/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/auth/register/` | No | Register a new Viewer account |
| POST | `/auth/login/` | No | Log in, receive JWT tokens |
| POST | `/auth/logout/` | Yes | Blacklist refresh token |
| POST | `/auth/token/refresh/` | No | Get new access token |
| GET | `/users/me/` | Yes | Get own profile |
| PATCH | `/users/me/` | Yes | Update own profile |

**Register example:**
```json
POST /api/v1/auth/register/
{
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "password": "SecurePass99!",
  "password_confirm": "SecurePass99!"
}
```

**Create User (Admin Only)**
````json
POST /api/v1/users/
{
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "password": "SecurePass99!",
  "role": "analyst"
}
````

**Login response includes user info:**
```json
{
  "access": "<jwt-access-token>",
  "refresh": "<jwt-refresh-token>",
  "user": {
    "id": "...",
    "email": "alice@example.com",
    "role": "VIEWER",
  }
}
```

All subsequent requests must include:
```
Authorization: Bearer <access-token>
```

---

### User Management — `/api/v1/users/` *(Admin only)*

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/` | List all users (search, filter by role/status) |
| POST | `/users/` | Create a new user with a specific role |
| GET | `/users/<id>/` | Get a user's detail |
| PATCH | `/users/<id>/` | Update role, name, or active status |
| DELETE | `/users/<id>/` | Deactivate a user (not physically deleted) |

**Query params for listing:**
```
?role=ANALYST           filter by role
?is_active=true         filter by status
?search=alice           search by name or email
?ordering=-date_joined  sort
```

---

### Financial Records — `/api/v1/records/`

| Method | Endpoint | Roles | Description |
|---|---|---|---|
| GET | `/records/` | All | List records with filters & pagination |
| POST | `/records/` | Admin | Create a financial record |
| GET | `/records/<id>/` | All | Get record detail |
| PATCH | `/records/<id>/` | Admin | Update a record |
| DELETE | `/records/<id>/` | Admin | Soft-delete a record |
| POST | `/records/<id>/restore/` | Admin | Restore a soft-deleted record |
| GET | `/records/categories/` | All | List all categories |
| POST | `/records/categories/` | Admin | Create a category |
| PATCH | `/records/categories/<id>/` | Admin | Update a category |
| DELETE | `/records/categories/<id>/` | Admin | Delete a category |

**Create record example:**
```json
POST /api/v1/records/
{
  "amount": "2500.00",
  "type": "INCOME",
  "category_id": "<category-uuid>",
  "date": "2024-06-15",
  "notes": "Client payment - June invoice"
}
```

**Filter query params:**
```
?type=INCOME
?type=EXPENSE
?date_from=2024-01-01
?date_to=2024-12-31
?category_id=<uuid>
?amount_min=100
?amount_max=5000
?search=salary              searches notes + category name
?ordering=-amount           sort by amount descending
?page=2&page_size=10        pagination
```

**Pagination response shape:**
```json
{
  "count": 84,
  "next": "...",
  "previous": null,
  "results": [...]
}
```

---

### Analytics — `/api/v1/analytics/` *(Analyst + Admin)*

| Method | Endpoint | Description |
|---|---|---|
| GET | `/analytics/summary/` | Total income, expenses, net balance |
| GET | `/analytics/categories/` | Per-category totals for pie charts |
| GET | `/analytics/trends/monthly/` | Monthly income vs expense for last N months |
| GET | `/analytics/recent/` | Latest N transactions |
| GET | `/analytics/split/` | Income vs expense percentage split |

**Summary response:**
````json
{
  "success": true,
  "message": "Success",
  "data": {
    "total_income": 45000.00,
    "total_expense": 18300.00,
    "balance": 26700.00,
    "count": 47
  }
}
````

**Monthly trends query params:**
```
?months=6       look back 6 months (default: 12, max: 36)
?weeks=4        look back 4 weeks  (default: 8,  max: 52)
?limit=5        recent activity    (default: 10, max: 50)
?date_from=...  filter summary by date range
?date_to=...
?type=INCOME    filter category breakdown by type
```

---

## Role-Based Access Control

| Action | VIEWER | ANALYST | ADMIN |
|---|:---:|:---:|:---:|
| View financial records | ✅ | ✅ | ✅ |
| View categories | ✅ | ✅ | ✅ |
| Access analytics & trends | ❌ | ✅ | ✅ |
| Create / update records | ❌ | ❌ | ✅ |
| Soft-delete / restore records | ❌ | ❌ | ✅ |
| Manage categories | ❌ | ❌ | ✅ |
| List / manage users | ❌ | ❌ | ✅ |
| View own profile (`/me`) | ✅ | ✅ | ✅ |

Access control is enforced via **DRF permission classes** in every view — no business logic bypasses it. The three permission classes are:

- `IsAdmin` — role must be `ADMIN`
- `IsAnalystOrAbove` — role must be `ANALYST` or `ADMIN`
- `IsViewer` — any authenticated user with a valid role

---

## Design Decisions & Assumptions

**1. Roles as a simple CharField, not a separate table**
The spec defines three fixed roles. A `Role` table would add complexity without benefit at this scope. If roles ever need to be dynamic or user-defined, migrating from `TextChoices` to a FK is straightforward.

**2. Soft-delete on FinancialRecord, not on User**
Financial records must never be permanently lost (audit trail). Users, however, are deactivated via `is_active=False` rather than soft-deleted — this aligns with how Django's auth system works and avoids complications with the user FK in records.

**3. Amount is always positive**
The `type` field (INCOME/EXPENSE) carries the directional meaning. Storing negative expenses would make aggregation queries more error-prone. The `signed_amount` property computes the signed value when needed.


**4. Future dates rejected at serializer level**
A financial transaction cannot occur in the future. This is validated in the serializer rather than the model so it returns a clean 400 validation error.

**5. Rate limits are per-scope**
- Authenticated users: 100/min
- Anonymous users: 20/min

**6. Assumption — single currency**
The spec does not mention multi-currency. Records store raw decimal amounts. Currency support would require adding a `currency` field and an exchange rate service.

---

## Optional Enhancements Implemented

| Enhancement | Implementation |
|---|---|
| ✅ JWT Authentication | SimpleJWT with access/refresh tokens, blacklist on logout, custom payload |
| ✅ Pagination | `StandardResultsPagination` with metadata on all list endpoints |
| ✅ Search | DRF `SearchFilter` on records (notes, category name) and users (name, email) |
| ✅ Soft Delete | `SoftDeleteModel` + `SoftDeleteManager` with restore endpoint |
| ✅ Rate Limiting | DRF throttling — `auth` scope (10/min), `user` scope (100/min) |
| ✅ Unit Tests | pytest + factory-boy, 30+ test cases across 3 files |
| ✅ Swagger API Docs | drf-spectacular at `/api/docs/` — interactive, auto-generated |
| ✅ Request Audit Logging | `RequestLoggingMiddleware` logs every request with user + timing |
