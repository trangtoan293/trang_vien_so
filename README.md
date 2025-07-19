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
Frontend (Web)    │ React + TypeScript + Tailwind CSS
Backend API       │ Node.js + Express + TypeScript  
Database          │ PostgreSQL (Supabase managed)
File Storage      │ Supabase Storage / AWS S3
Authentication    │ Supabase Auth + JWT
Hosting           │ Railway / Render / Vercel
```

### Simplified Architecture
```
┌─────────────────────────────────────────┐
│         React Web App (PWA)             │
│         Mobile-Responsive               │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│      Express.js API Server              │
│   Auth │ File Upload │ Business Logic   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│  PostgreSQL │ Redis │ File Storage      │
│  (Main Data)│(Cache)│ (Media Files)     │
└─────────────────────────────────────────┘
```

## 📂 Cấu Trúc Dự Án

```
trang_vien_so/
├── docs/                    # 📋 Tài liệu dự án
│   ├── BRD.md              # Business Requirements
│   ├── Customer_Journey.md  # User journey mapping
│   ├── Features.md         # Feature specifications
│   ├── Planning.md         # Implementation planning
│   └── Task.md            # Task breakdown
├── frontend/               # 🎨 React web application
├── backend/                # ⚙️ Express.js API server
├── shared/                 # 🔄 Shared types và utilities
├── docs/api/              # 📚 API documentation
└── deployment/            # 🚀 Deployment configurations
```

## 🚀 Bắt Đầu

### Prerequisites
- Node.js 18+ và npm/yarn
- PostgreSQL (hoặc Supabase account)
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/trangtoan293/trang_vien_so.git
cd trang_vien_so

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env với database và API keys

# Start development servers
npm run dev        # Starts both frontend and backend
npm run dev:frontend  # Frontend only (port 3000)
npm run dev:backend   # Backend only (port 8000)
```

### Environment Setup
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/trang_vien_so
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# Authentication
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRES_IN=24h

# File Storage
AWS_S3_BUCKET=your_s3_bucket
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Email Service
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

## 👥 Team & Workflow

### Core Team (4-5 người)
- **Product Owner** (1): Requirements, testing, stakeholder management
- **Frontend Developer** (1-2): React development, UI/UX implementation
- **Backend Developer** (1-2): API development, database design
- **DevOps/Full-stack** (1): Infrastructure, deployment, QA support

### Development Workflow
1. **Sprint Planning**: 4-week sprints với clear deliverables
2. **Code Quality**: ESLint, Prettier, testing requirements
3. **Git Workflow**: Feature branches → PR review → main branch
4. **Deployment**: Automated CI/CD với GitHub Actions

## 📋 Roadmap

### Phase 1: Web MVP (Months 1-3)
- [x] User authentication và profile management
- [x] Deceased profile creation với Vietnamese features
- [x] Media upload và gallery
- [x] Basic family tree visualization
- [x] Sharing và privacy controls
- [ ] **In Progress**: Sprint 1-2 foundation setup

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
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Lint code
npm run lint

# Type checking
npm run type-check
```

### Testing Strategy
- **Unit Tests**: 90%+ coverage với Jest
- **Integration Tests**: API endpoints và database operations
- **E2E Tests**: Cypress cho user workflows
- **Accessibility**: WCAG 2.1 AA compliance testing

## 🔐 Security & Privacy

### Data Protection
- End-to-end encryption cho sensitive data
- HTTPS everywhere với TLS 1.3
- Regular security audits và penetration testing
- GDPR compliance với right to be forgotten

### Authentication
- Multi-factor authentication
- Role-based access control (Admin, Editor, Viewer)
- Session management với JWT refresh tokens
- OAuth2 integration (Google, Facebook)

## 📈 Monitoring & Analytics

- **Performance**: Load time <3s, API response <200ms
- **Uptime**: 99.9% availability target
- **User Metrics**: MAU, retention, feature adoption
- **Error Tracking**: Sentry integration

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