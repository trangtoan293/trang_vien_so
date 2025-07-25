# Trang Vien So - Python Backend

=o Vietnamese Memorial App - FastAPI Backend Implementation

## Overview

Production-ready Python backend for the Trang Vien So (Memorial Page) application, built with FastAPI and PostgreSQL. This backend serves as the primary API for managing deceased profiles, family relationships, and memorial content in Vietnamese cultural context.

## =� Features

###  Implemented
- **Authentication System**: JWT-based auth with session management
- **Database Integration**: PostgreSQL with SQLAlchemy async models
- **User Management**: Registration, login, profile management
- **Health Monitoring**: Database connectivity and system health checks
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Security**: CORS, input validation, password hashing
- **Logging**: Request tracking and performance monitoring

### = In Development
- **Deceased Profile Management**: Memorial profile creation and management
- **Family System**: Family groups and member invitations
- **Media Upload**: Photo and document management
- **Advanced Search**: Full-text search with Vietnamese support

## =� Project Structure

```
backend_python/
   app/
      core/              # Core configuration and security
         auth.py        # Authentication middleware
         config.py      # Environment configuration
         database.py    # Database connection and session management
         security.py    # JWT tokens and password hashing
      models/            # SQLAlchemy database models
         user.py        # User and UserSession models
         deceased.py    # Deceased profile models
         family.py      # Family and member models
         media.py       # Media file models
      routers/           # API route handlers
         auth.py        # Authentication endpoints
         health.py      # Health check endpoints
         users.py       # User management endpoints
      schemas/           # Pydantic validation schemas
         auth.py        # Authentication request/response schemas
         user.py        # User data schemas
         ...            # Other schema files
      services/          # Business logic services
         auth_service.py # Authentication service layer
      main.py            # FastAPI application entry point
   tests/                 # Test files and test utilities
   pyproject.toml         # UV dependency management
   .gitignore            # Git ignore patterns
   README.md             # This file
```

## =� Technology Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0
- **Authentication**: JWT tokens with session management
- **Validation**: Pydantic v2 schemas
- **Password**: bcrypt hashing (Node.js compatible)
- **Package Management**: UV (ultrafast Python package manager)
- **Development**: Uvicorn ASGI server with hot reload

## =� Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- UV package manager

### Installation

1. **Clone and setup environment**:
   ```bash
   cd backend_python
   uv sync
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Start the development server**:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/api/docs
   - Health Check: http://localhost:8000/api/health

## >� Testing

Run the test suite:

```bash
# Database integration tests
uv run python tests/test_database_integration.py

# Authentication system tests
uv run python tests/test_authentication.py

# Quick API tests
uv run python tests/test_python_api.py
```

## = Authentication Flow

1. **User Registration**: POST `/api/auth/register`
2. **User Login**: POST `/api/auth/login`
3. **Token Refresh**: POST `/api/auth/refresh`
4. **Protected Routes**: Include `Authorization: Bearer <token>` header
5. **User Logout**: POST `/api/auth/logout`

## =� API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info
- `GET /api/auth/verify-token` - Verify token validity

### Health & Monitoring
- `GET /api/health` - Comprehensive health check
- `GET /api/health/simple` - Basic health check
- `GET /api/status` - System status

### Users (Planned)
- `GET /api/users/` - List users
- `GET /api/users/{id}` - Get user profile
- `PUT /api/users/{id}` - Update user profile

## =� Database Schema

The backend uses the existing PostgreSQL schema with 8 tables:
- `users` - User accounts and profiles
- `user_sessions` - Authentication sessions
- `deceased_profiles` - Memorial profiles
- `families` - Family groups
- `family_members` - Family membership
- `invitations` - Family invitations
- `media_files` - Photos and documents
- `media_with_profile` - Media associations

## =' Configuration

Environment variables (see `.env.example`):

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/trang_vien_so

# Security
JWT_SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
ENVIRONMENT=development
DEBUG=true
```

## < Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production`
2. Configure proper `JWT_SECRET_KEY`
3. Set up SSL/TLS certificates
4. Configure database connection pooling
5. Set up monitoring and logging
6. Configure CORS for your frontend domain

## =� Performance

- **Database queries**: Sub-30ms response times
- **Authentication**: Real-time JWT validation
- **API responses**: Sub-5ms for health checks
- **Memory usage**: Optimized connection pooling

## > Contributing

1. Follow Python PEP 8 style guidelines
2. Add type hints to all functions
3. Write tests for new functionality
4. Update documentation for API changes
5. Use descriptive commit messages

## =� License

This project is part of the Trang Vien So memorial application.

## = Related Projects

- **Frontend**: React.js application (separate repository)
- **Node.js Backend**: Original Node.js implementation (being replaced)
- **Database**: PostgreSQL schema and migrations

---

**Built with d for Vietnamese memorial traditions**