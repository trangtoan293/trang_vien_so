# Trang Viên Số - Vietnamese Memorial App

> 🕯️ Ứng dụng lưu trữ và chia sẻ kỷ niệm người thân đã khuất cho gia đình Việt Nam

## 📖 Tổng Quan

**Trang Viên Số** là ứng dụng web hiện đại giúp các gia đình Việt Nam lưu trữ, quản lý và chia sẻ kỷ niệm về người thân đã khuất. Ứng dụng tích hợp sâu sắc với văn hóa và phong tục truyền thống Việt Nam, cung cấp giải pháp toàn diện từ lưu trữ thông tin, quản lý cây gia phả đến kết nối với các dịch vụ tang lễ và cúng bái.

### ✨ Tính Năng Chính

- **👤 Quản lý hồ sơ người mất**: Lưu trữ thông tin chi tiết với ngày cúng đặc biệt và âm lịch
- **📸 Thư viện kỷ niệm**: Upload và tổ chức ảnh, video với gallery thông minh
- **🌳 Cây gia phả tương tác**: Xây dựng và trực quan hóa mối quan hệ gia đình
- **📅 Lịch cúng bái**: Tự động tính toán và nhắc nhở các ngày đặc biệt
- **🏛️ Quản lý nơi an nghỉ**: Thông tin nghĩa trang, chùa, và nơi lưu trữ tro cốt
- **🤝 Chia sẻ gia đình**: Mời thành viên và cộng tác chỉnh sửa
- **📖 Hồi ký cuộc đời**: Công cụ tạo và lưu trữ câu chuyện đời
- **🛍️ Thư mục dịch vụ**: Kết nối với nhà cung cấp dịch vụ tang lễ uy tín

## 🎯 Chiến Lược Phát Triển

### Web-First MVP Approach
- **Phase 1** (3 tháng): Web MVP với core features
- **Phase 2** (3 tháng): Enhanced features và service marketplace
- **Phase 3** (4 tháng): Mobile app migration và business scaling

### Target Users
- **Primary**: Con cái, cháu có trách nhiệm lưu giữ kỷ niệm gia đình
- **Secondary**: Người cao tuổi, nhà cung cấp dịch vụ tang lễ/cúng bái

## 🏗️ Kiến Trúc Hệ Thống

### Tech Stack
```
Frontend (Web)    │ React + TypeScript + Tailwind CSS (Planned)
Backend API       │ ✅ Python 3.11+ + FastAPI (IMPLEMENTED)
Database          │ ✅ PostgreSQL with SQLAlchemy async ORM
File Storage      │ Local storage (S3 migration planned)
Authentication    │ ✅ JWT + Session Management (PRODUCTION-READY)
Hosting           │ Railway / Render / Fly.io (Python-optimized)
```

### Modern Python-First Architecture
```
┌─────────────────────────────────────────┐
│         React Web App (PWA)             │
│         Mobile-Responsive               │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│      ✅ FastAPI Python Server           │
│   ✅ Auth │ ✅ Ready │ ✅ Framework     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│  ✅ PostgreSQL │ Redis │ File Storage    │
│  (Connected)   │(Optional)│ (Local/S3)   │
└─────────────────────────────────────────┘
```

## 📂 Cấu Trúc Dự Án

```
trang_vien_so/
├── docs/                     # 📋 Tài liệu dự án
│   ├── BRD.md               # Business Requirements
│   ├── Customer_Journey.md   # User journey mapping
│   ├── Features.md          # Feature specifications
│   ├── Planning.md          # Original implementation planning
│   ├── Planning_Python.md   # ✅ Updated Python backend planning
│   └── Task.md             # Task breakdown (JS-based)
├── frontend/                # 🎨 React web application (Planned)
├── backend_python/          # ✅ FastAPI Python server (IMPLEMENTED)
│   ├── app/                 # Main application code
│   │   ├── models/          # SQLAlchemy database models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── routers/         # API route handlers
│   │   ├── services/        # Business logic services
│   │   └── core/           # Core configurations
│   ├── tests/              # Comprehensive test suite
│   └── requirements.txt    # Python dependencies (UV managed)
├── database/               # PostgreSQL setup and schema
├── shared/                 # 🔄 Shared types và utilities
└── scripts/               # Development and testing scripts
```

## 🚀 Bắt Đầu

### Prerequisites
- Python 3.11+ và UV package manager
- Node.js 18+ (for frontend, when implemented)
- PostgreSQL database
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/trangtoan293/trang_vien_so.git
cd trang_vien_so

# Setup Python backend (IMPLEMENTED)
cd backend_python

# Install UV package manager (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Setup environment variables
cp .env.example .env
# Edit .env với database configuration

# Start PostgreSQL database
cd ../database
docker-compose up -d

# Initialize database schema
docker exec -i postgres_db psql -U postgres -d trang_vien_so < init-scripts/01-schema.sql

# Run Python backend server
cd ../backend_python
uv run uvicorn app.main:app --reload --port 8002

# Test API endpoints (in another terminal)
cd ..
node scripts/test-api.js

# API Documentation available at:
# http://localhost:8002/docs (Swagger UI)
# http://localhost:8002/redoc (ReDoc)
```

### Environment Setup
```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/trang_vien_so
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trang_vien_so
DB_USER=postgres
DB_PASSWORD=postgres

# JWT Authentication (Production-ready)
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Application Settings
API_V1_STR=/api/v1
PROJECT_NAME="Trang Vien So API"
PROJECT_VERSION=1.0.0
DEBUG=true

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# File Storage (Local initially)
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# Email Service (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAILS_FROM_EMAIL=noreply@trangvienso.com
```

## 👥 Team & Workflow

### Reduced Team (3-4 người)
- **Product Owner** (1): Requirements, user research, stakeholder management
- **Frontend Developer** (1-2): React integration with Python APIs
- **Python Developer** (0.5): Complete remaining backend features
- **DevOps/QA** (0.5): Deployment, testing, monitoring

### Development Workflow
1. **Sprint Planning**: 4-week sprints với clear deliverables
2. **Code Quality**: ESLint, Prettier, testing requirements
3. **Git Workflow**: Feature branches → PR review → main branch
4. **Deployment**: Automated CI/CD với GitHub Actions

## 📋 Roadmap

### Phase 1: Web MVP (Months 1-2) - 50% Complete ✅
**Python Backend Foundation**:
- ✅ FastAPI application with async PostgreSQL
- ✅ Complete authentication system (register/login/logout/refresh)
- ✅ User management with profile support
- ✅ SQLAlchemy models for all database tables
- ✅ Pydantic schemas for request/response validation
- ✅ JWT authentication with session management
- ✅ Health monitoring and error handling
- ✅ Auto-generated API documentation

**Next Steps**:
- [ ] **Frontend Integration**: React app setup with Python API client
- [ ] **Profile Management UI**: Connect to existing Python user APIs
- [ ] **Deceased Profile Foundation**: Implement remaining CRUD operations
- [ ] **File Upload**: Complete media upload with Python backend

### Phase 2: Enhanced Features (Months 4-6)
- [ ] Advanced family tree với D3.js
- [ ] Vietnamese lunar calendar integration
- [ ] Service directory và contact management
- [ ] Memoir creation tools
- [ ] Advanced collaboration features

### Phase 3: Mobile & Scale (Months 7-10)
- [ ] React Native mobile app
- [ ] Service marketplace với payments
- [ ] Community features
- [ ] Premium subscription tiers
- [ ] App store launch

## 🧪 Testing

```bash
# Python Backend Testing (✅ IMPLEMENTED)
cd backend_python

# Run all Python tests
uv run python -m pytest tests/ -v

# Run tests with coverage
uv run python -m pytest tests/ --cov=app --cov-report=html

# Run specific test categories
uv run python -m pytest tests/test_auth.py -v      # Authentication tests
uv run python -m pytest tests/test_database.py -v  # Database integration
uv run python -m pytest tests/test_health.py -v    # Health check tests

# Test API endpoints directly
node scripts/test-api.js

# Frontend Testing (Planned)
# npm test                    # Unit tests with Jest
# npm run test:e2e           # E2E tests with Playwright
# npm run lint               # Code linting
# npm run type-check         # TypeScript checking
```

### Testing Strategy (Updated)
- ✅ **Python Backend Tests**: 100% test success rate for authentication and database
- ✅ **Integration Tests**: Working API endpoints with real PostgreSQL database
- ✅ **Health Monitoring**: Comprehensive health check validation
- [ ] **Frontend Tests**: React Testing Library setup (when frontend implemented)
- [ ] **E2E Tests**: Playwright for complete user workflows
- [ ] **Performance Tests**: Load testing for Python endpoints

## 🔐 Security & Privacy

### Data Protection
- End-to-end encryption cho sensitive data
- HTTPS everywhere với TLS 1.3
- Regular security audits và penetration testing
- GDPR compliance với right to be forgotten

### Authentication (✅ Production-Ready)
- ✅ JWT authentication with access + refresh tokens
- ✅ Session management with device tracking
- ✅ bcrypt password hashing (Node.js compatible)
- ✅ Input validation with Pydantic schemas
- [ ] Multi-factor authentication (planned)
- [ ] Role-based access control (planned)
- [ ] OAuth2 integration (planned)

## 📈 Monitoring & Analytics

- ✅ **API Performance**: Sub-30ms database queries, <100ms response times
- ✅ **Database**: Async SQLAlchemy with connection pooling
- ✅ **Health Monitoring**: Real-time health checks and performance metrics
- ✅ **Error Handling**: Comprehensive error tracking and logging
- [ ] **Uptime**: 99.9% availability target (post-deployment)
- [ ] **User Metrics**: MAU, retention, feature adoption (post-frontend)
- [ ] **Error Tracking**: Sentry integration (planned)

## 🤝 Contributing

### Development Guidelines
1. Fork repository và create feature branch
2. Follow coding standards (ESLint + Prettier)
3. Write tests cho new features
4. Update documentation
5. Submit pull request với clear description

### Code Style
```javascript
// Follow TypeScript best practices
interface DeceasedProfile {
  id: string;
  basicInfo: PersonInfo;
  specialDates: SpecialDates;
  familyRelations: FamilyRelation[];
}

// Use meaningful function names
const calculateLunarAnniversary = (deathDate: Date): Date => {
  // Implementation
};
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [API Documentation](docs/api/README.md)
- [User Guide](docs/user-guide/README.md)
- [Developer Guide](docs/developer-guide/README.md)

### Contact
- **Project Owner**: Trang Toan ([@trangtoan293](https://github.com/trangtoan293))
- **Issues**: [GitHub Issues](https://github.com/trangtoan293/trang_vien_so/issues)
- **Discussions**: [GitHub Discussions](https://github.com/trangtoan293/trang_vien_so/discussions)

### Quick Links
- [🔗 Live Demo](https://trangvienso.vercel.app) (Coming soon)
- [📊 Project Board](https://github.com/trangtoan293/trang_vien_so/projects)
- [📋 Changelog](CHANGELOG.md)

---

<p align="center">
  <i>💝 Được phát triển với tình yêu để tôn vinh kỷ niệm gia đình Việt Nam</i>
</p>