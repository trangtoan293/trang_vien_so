# Implementation Planning - Ứng Dụng Lưu Trữ Kỷ Niệm Người Đã Mất

## Executive Summary

Dự án xây dựng ứng dụng **web-first** giúp gia đình Việt Nam lưu trữ, quản lý và chia sẻ kỷ niệm về người thân đã khuất. Strategy là MVP web app trước để validate market fit, sau đó migrate sang mobile app.

**Timeline**: 8-10 tháng (3 phases)  
**Budget Estimate**: $80,000 - $120,000  
**Team Size**: 4-5 người  
**Launch Strategy**: Web MVP → User validation → Mobile migration → Scale

---

## System Architecture

### Simplified Architecture cho Small Team

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                          │
├─────────────────────────────────────────────────────────┤
│      React Web App (PWA)      │    Admin Dashboard      │
│      Mobile-Responsive        │    Content Management   │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                MONOLITHIC API SERVER                     │
├─────────────────────────────────────────────────────────┤
│  Express.js + TypeScript                                │
│  Authentication │ File Upload │ Business Logic │ APIs    │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                             │
├─────────────────────────────────────────────────────────┤
│  PostgreSQL    │    Redis     │    File Storage          │
│  (Main Data)   │   (Cache)    │   (AWS S3/Supabase)     │
└─────────────────────────────────────────────────────────┘
```

**Future Migration Path**:
- Phase 3: Add React Native mobile app
- Phase 4: Microservices split khi scale >10K users

### Technical Stack Recommendation

#### Frontend (Web-First)
- **Web App**: React.js + TypeScript (PWA-ready)
- **Build Tool**: Vite (faster development)
- **State Management**: Zustand (lighter than Redux)
- **UI Framework**: Tailwind CSS + Headless UI
- **Navigation**: React Router v6

#### Backend (Simplified)
- **Runtime**: Node.js + Express.js
- **Language**: TypeScript
- **API**: RESTful API (GraphQL sau khi có mobile)
- **Authentication**: Passport.js + JWT
- **File Processing**: Sharp (images only initially)

#### Database (Minimal Viable)
- **Primary**: PostgreSQL (managed via Supabase)
- **Cache**: Redis (small instance)
- **File Storage**: Supabase Storage hoặc AWS S3
- **Search**: PostgreSQL full-text search (ElasticSearch sau)

#### Infrastructure (Cost-Effective)
- **Hosting**: Railway / Render / Vercel (easy deployment)
- **Database**: Supabase (managed PostgreSQL)
- **CI/CD**: GitHub Actions
- **Monitoring**: Basic error tracking (Sentry)
- **Domain**: Custom domain với SSL

#### Security (Essential)
- **Authentication**: Supabase Auth hoặc Passport.js
- **Encryption**: HTTPS everywhere, bcrypt passwords
- **API Security**: Rate limiting, input validation
- **Compliance**: Basic GDPR compliance

---

## Development Roadmap

### Phase 1: Web MVP (Months 1-3)
**Goal**: Validate product-market fit với web application

#### Sprint 1-2: Foundation & Authentication (4 weeks)
- [ ] Project setup với modern web stack
- [ ] PostgreSQL database design
- [ ] User authentication system
- [ ] Basic responsive UI framework
- [ ] Deployment pipeline

#### Sprint 3-4: Core Features (4 weeks)
- [ ] Deceased profile creation/editing
- [ ] Photo upload và basic gallery
- [ ] Simple family relationships
- [ ] Basic privacy controls

#### Sprint 5-6: Sharing & Polish (4 weeks)
- [ ] Family member invitation system
- [ ] Share links functionality
- [ ] UI/UX polish cho elderly users
- [ ] Basic search và filtering

**Success Metrics**: 
- 100 beta users trong tháng 3
- 80% profile completion rate
- 4.0+ user satisfaction score

### Phase 2: Enhanced Web Features (Months 4-6)
**Goal**: Advanced features để increase user engagement

#### Sprint 7-8: Advanced Family Tree (4 weeks)
- [ ] Visual family tree với D3.js
- [ ] Complex relationship handling
- [ ] Tree export functionality
- [ ] Collaborative editing

#### Sprint 9-10: Calendar & Reminders (4 weeks)
- [ ] Vietnamese lunar calendar
- [ ] Automated reminders
- [ ] Email notification system
- [ ] Custom events management

#### Sprint 11-12: Service Directory (4 weeks)
- [ ] Basic service provider listing
- [ ] Contact information management
- [ ] Simple review system
- [ ] Location-based search

**Success Metrics**:
- 1,000 active users
- 60% monthly retention
- Advanced features adoption >50%

### Phase 3: Mobile Migration & Scale (Months 7-10)
**Goal**: Mobile app launch và business scaling

#### Sprint 13-16: Mobile Development (8 weeks)
- [ ] React Native app setup
- [ ] Core features migration
- [ ] Mobile-specific features (camera, GPS)
- [ ] App store submission

#### Sprint 17-20: Business Features (8 weeks)
- [ ] Service marketplace với payments
- [ ] Premium features (unlimited storage)
- [ ] Advanced analytics
- [ ] Community features (forums)

**Success Metrics**:
- 5,000+ mobile app downloads
- 10,000+ total users
- $10,000+ monthly revenue

---

## Core Module Specifications

### 1. User Management Service
**Responsibilities**: Authentication, user profiles, role management

**Key Features**:
- Multi-factor authentication
- Role-based access control (Family Admin, Member, Viewer)
- Social login integration
- Profile management
- Privacy settings

**APIs**:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `POST /api/users/invite` - Invite family member

### 2. Content Management Service
**Responsibilities**: Media files, profiles, content versioning

**Key Features**:
- Multi-format media support (images, videos, documents)
- Content versioning
- Bulk upload/download
- Media optimization
- CDN integration

**APIs**:
- `POST /api/content/upload` - Upload media files
- `GET /api/content/{id}` - Get content by ID
- `DELETE /api/content/{id}` - Delete content
- `PUT /api/content/{id}/metadata` - Update metadata

### 3. Family Tree Service
**Responsibilities**: Relationship mapping, tree visualization

**Key Features**:
- Complex relationship modeling
- Visual tree generation
- Collaborative editing
- Conflict resolution
- Export capabilities

**APIs**:
- `GET /api/family-tree/{familyId}` - Get family tree
- `POST /api/family-tree/relationships` - Add relationship
- `PUT /api/family-tree/relationships/{id}` - Update relationship
- `DELETE /api/family-tree/relationships/{id}` - Delete relationship

### 4. Location Service
**Responsibilities**: Cemetery/temple directory, GPS integration

**Key Features**:
- Location database
- GPS coordinates
- Custom location addition
- Distance calculation
- Map integration

**APIs**:
- `GET /api/locations/cemeteries` - Get cemetery list
- `GET /api/locations/temples` - Get temple list
- `POST /api/locations/custom` - Add custom location
- `GET /api/locations/nearby` - Find nearby locations

### 5. Service Marketplace
**Responsibilities**: Service providers, bookings, payments

**Key Features**:
- Provider directory
- Service catalog
- Booking system
- Payment processing
- Rating/review system

**APIs**:
- `GET /api/services/providers` - Get service providers
- `POST /api/services/bookings` - Create booking
- `GET /api/services/bookings/{id}` - Get booking details
- `PUT /api/services/bookings/{id}/status` - Update booking status

### 6. Notification Service
**Responsibilities**: Reminders, alerts, communication

**Key Features**:
- Calendar integration
- Smart scheduling
- Multiple channels (push, email, SMS)
- Preference management
- Delivery tracking

**APIs**:
- `GET /api/notifications` - Get notifications
- `POST /api/notifications/schedule` - Schedule notification
- `PUT /api/notifications/{id}/read` - Mark as read
- `DELETE /api/notifications/{id}` - Delete notification

### 7. Memoir Service
**Responsibilities**: Life story creation, rich content

**Key Features**:
- Rich text editor
- Template system
- Media integration
- Export formats (PDF, HTML)
- Sharing capabilities

**APIs**:
- `GET /api/memoirs/{profileId}` - Get memoir
- `PUT /api/memoirs/{profileId}` - Update memoir
- `POST /api/memoirs/{profileId}/export` - Export memoir
- `GET /api/memoirs/templates` - Get templates

---

## Data Models

### User Model
```javascript
{
  id: UUID,
  email: String,
  phone: String,
  profile: {
    firstName: String,
    lastName: String,
    dateOfBirth: Date,
    avatar: String,
    bio: String
  },
  settings: {
    language: String,
    notifications: Object,
    privacy: Object
  },
  createdAt: Date,
  updatedAt: Date
}
```

### Deceased Profile Model
```javascript
{
  id: UUID,
  basicInfo: {
    firstName: String,
    lastName: String,
    dateOfBirth: Date,
    dateOfDeath: Date,
    placeOfBirth: String,
    placeOfDeath: String,
    causeOfDeath: String
  },
  specialDates: {
    deathAnniversary: Date,
    worship49Days: Date,
    worship100Days: Date,
    customDates: Array
  },
  media: {
    photos: Array,
    videos: Array,
    documents: Array
  },
  memoir: {
    content: String,
    lastUpdated: Date,
    contributors: Array
  },
  location: {
    cemetery: String,
    temple: String,
    customLocation: String,
    coordinates: {
      lat: Number,
      lng: Number
    }
  },
  familyId: UUID,
  privacy: {
    visibility: String,
    allowedUsers: Array
  },
  createdBy: UUID,
  createdAt: Date,
  updatedAt: Date
}
```

### Family Tree Model (Neo4j)
```javascript
// Person Node
{
  id: UUID,
  name: String,
  dateOfBirth: Date,
  dateOfDeath: Date,
  isDeceased: Boolean,
  profileId: UUID
}

// Relationship Edge
{
  type: String, // "PARENT", "SPOUSE", "SIBLING", "CHILD"
  startDate: Date,
  endDate: Date,
  notes: String
}
```

---

## Security Requirements

### Data Protection
- **Encryption at Rest**: AES-256 encryption cho sensitive data
- **Encryption in Transit**: TLS 1.3 cho all API communications
- **Zero-Knowledge Architecture**: Một số data types chỉ user mới decrypt được
- **Regular Security Audits**: Quarterly penetration testing

### Authentication & Authorization
- **Multi-Factor Authentication**: SMS/Email verification
- **Role-Based Access Control**: Family Admin, Member, Viewer roles
- **Session Management**: JWT tokens với refresh mechanism
- **OAuth2 Integration**: Google, Facebook, Apple sign-in

### API Security
- **Rate Limiting**: 100 requests/minute per user
- **Input Validation**: Comprehensive validation cho all inputs
- **SQL Injection Prevention**: Parameterized queries
- **CORS Configuration**: Strict cross-origin policies

### Privacy Compliance
- **GDPR Compliance**: Right to be forgotten, data portability
- **Data Retention**: Configurable retention policies
- **Audit Logging**: Complete audit trail cho sensitive operations
- **Anonymous Analytics**: No PII trong analytics data

---

## Testing Strategy

### Unit Testing
- **Coverage Target**: 90%+ code coverage
- **Framework**: Jest (Node.js), React Testing Library
- **Focus Areas**: Business logic, API endpoints, utility functions
- **Automation**: Run on every commit

### Integration Testing
- **API Testing**: Postman/Newman automated tests
- **Database Testing**: Test với real database instances
- **Service Integration**: Test interactions between services
- **File Upload Testing**: Test large file handling

### End-to-End Testing
- **Framework**: Cypress / Playwright
- **User Journeys**: Test complete user workflows
- **Cross-Platform**: iOS, Android, Web testing
- **Performance**: Load testing với Artillery.js

### User Acceptance Testing
- **Beta Testing**: 50 families testing trong 4 weeks
- **Usability Testing**: Đặc biệt focus on elderly users
- **Cultural Sensitivity**: Test với various Vietnamese regions
- **Accessibility**: WCAG 2.1 AA compliance

---

## Risk Management

### Technical Risks
**Risk**: Complex family tree relationships causing performance issues
**Mitigation**: Use Neo4j graph database, implement caching, optimize queries

**Risk**: Large media files affecting app performance
**Mitigation**: Implement progressive loading, image optimization, CDN usage

**Risk**: Real-time collaboration conflicts
**Mitigation**: Implement operational transformation, conflict resolution algorithms

### Business Risks
**Risk**: Low adoption rate among elderly users
**Mitigation**: Extensive UX testing, simplified interface, tutorial system

**Risk**: Cultural sensitivity issues
**Mitigation**: Cultural consultant involvement, community feedback integration

**Risk**: Competition từ existing platforms
**Mitigation**: Focus on Vietnamese market, unique features, strong community

### Security Risks
**Risk**: Data breaches exposing sensitive family information
**Mitigation**: Multi-layer security, regular audits, incident response plan

**Risk**: Privacy concerns limiting adoption
**Mitigation**: Transparent privacy policy, granular controls, security education

---

## Team Structure & Roles

### Core Team (4-5 people)
- **Product Owner** (1): Requirements, user research, stakeholder management
- **Frontend Developer** (1-2): React web app, responsive design, UI/UX
- **Backend Developer** (1-2): API development, database, authentication
- **Full-stack/DevOps** (1): Infrastructure, deployment, testing support

### Responsibilities Distribution:
- **Product Owner**: Feature specs, user testing, market validation
- **Frontend**: React app, mobile-responsive design, state management
- **Backend**: APIs, database design, authentication, file handling
- **DevOps**: Hosting, CI/CD, monitoring, security basics

### Extended Support (contractors/part-time)
- **UI/UX Designer**: Design system, user research cho elderly users
- **Cultural Consultant**: Vietnamese traditions validation
- **Security Review**: Code review cho sensitive features

---

## Success Metrics & KPIs

### Technical Metrics
- **App Performance**: Load time <3 seconds
- **API Response Time**: <200ms average
- **Uptime**: 99.9% availability
- **Security**: Zero critical vulnerabilities
- **Test Coverage**: >90% code coverage

### Business Metrics
- **Phase 1**: 100 beta users, 80% profile completion
- **Phase 2**: 1,000 active users, 60% retention
- **Phase 3**: 10,000 total users, $10,000 MRR
- **Content Creation**: 3+ profiles per user average
- **Family Engagement**: 50% invite family members

### User Experience Metrics
- **App Store Rating**: 4.5+ stars
- **User Satisfaction**: 85%+ satisfaction score
- **Support Tickets**: <2% of users requiring support
- **Feature Adoption**: 80%+ of users using core features

---

## Budget Estimate

### Development Costs (10 months)
- **Team Salaries**: $60,000 (4-5 person Vietnam team)
- **Infrastructure**: $6,000 (Supabase, hosting, domains)
- **Third-party Services**: $3,000 (email, analytics, security)
- **Design & Legal**: $8,000 (UI/UX, legal consultation)
- **Testing & Marketing**: $3,000 (tools, beta testing, initial marketing)

**Total Estimated Cost**: $80,000

### Monthly Operational Costs (post-launch)
- **Infrastructure**: $500/month (managed services)
- **Third-party Services**: $300/month
- **Support & Maintenance**: $2,000/month
- **Marketing**: $1,000/month

**Total Monthly Cost**: $3,800

---

## Next Steps

1. **Immediate Actions** (Week 1-2):
   - Finalize team hiring
   - Setup development environment
   - Create detailed technical specifications
   - Begin UI/UX design process

2. **Short-term Goals** (Month 1):
   - Complete system architecture design
   - Setup CI/CD pipeline
   - Begin Sprint 1 development
   - Conduct user research interviews

3. **Medium-term Goals** (Month 3):
   - Complete MVP features
   - Begin beta testing
   - Implement security measures
   - Setup monitoring systems

4. **Long-term Goals** (Month 6):
   - Launch Phase 2 features
   - Expand user base
   - Implement monetization
   - Plan international expansion

---

*This planning document will be updated monthly based on progress, user feedback, and market conditions.*