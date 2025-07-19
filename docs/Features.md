# Feature Specifications - Memorial App MVP

## Overview

Tài liệu này định nghĩa chi tiết các tính năng cho MVP của ứng dụng lưu trữ kỷ niệm người đã mất, được thiết kế dựa trên BRD và Customer Journey analysis.

**MVP Strategy**: Web-first approach với focus trên core functionality cho user validation và product-market fit.

---

## Feature Prioritization (MoSCoW Method)

### Must Have (MVP Phase 1) - 3 tháng
✅ **F01**: User Authentication & Registration  
✅ **F02**: User Profile Management  
✅ **F03**: Deceased Profile Creation  
✅ **F04**: Media Upload & Gallery  
✅ **F05**: Basic Family Tree  
✅ **F06**: Basic Sharing & Privacy  

### Should Have (Phase 2) - 2-3 tháng
⚡ **F07**: Advanced Family Tree Features  
⚡ **F08**: Calendar & Reminders  
⚡ **F09**: Location Management  
⚡ **F10**: Basic Service Directory  
⚡ **F11**: Memoir Creation Tools  

### Could Have (Phase 3) - 3+ tháng
🔮 **F12**: Service Marketplace  
🔮 **F13**: Community Features  
🔮 **F14**: Advanced Analytics  
🔮 **F15**: Mobile App Migration  
🔮 **F16**: Premium Features  

### Won't Have (v1.0)
❌ AI-powered recommendations  
❌ Third-party API integrations  
❌ Advanced payment processing  
❌ Multi-language support (beyond Vietnamese)  

---

## Phase 1: Must Have Features (MVP)

### F01: User Authentication & Registration
**Epic**: Secure user onboarding và account management

#### User Stories:
- **US01.1**: Tôi muốn đăng ký account với email để có thể sử dụng app
- **US01.2**: Tôi muốn đăng nhập với email/password để truy cập vào data của mình
- **US01.3**: Tôi muốn reset password khi quên để lấy lại quyền truy cập
- **US01.4**: Tôi muốn đăng nhập với Google/Facebook để tiết kiệm thời gian

#### Acceptance Criteria:
**AC01.1** - User Registration:
- [ ] User có thể đăng ký với email, password, họ tên
- [ ] Password phải ≥8 ký tự, có chữ hoa, số
- [ ] Email verification required trước khi activate account
- [ ] Hiển thị clear error messages khi validation fail
- [ ] Redirect đến onboarding flow sau successful registration

**AC01.2** - User Login:
- [ ] User có thể login với email/password
- [ ] Remember me option để maintain session
- [ ] Lockout account sau 5 failed attempts
- [ ] Session expires sau 24h inactive
- [ ] Redirect đến dashboard sau successful login

**AC01.3** - Password Reset:
- [ ] User có thể request password reset via email
- [ ] Reset token expires sau 1 hour
- [ ] New password follows security requirements
- [ ] Invalidate all existing sessions sau password change

**AC01.4** - Social Login:
- [ ] Google OAuth2 integration
- [ ] Facebook OAuth2 integration
- [ ] Auto-create profile từ social data
- [ ] Link/unlink social accounts từ settings

#### Technical Specifications:
- **Authentication**: JWT tokens với refresh mechanism
- **Security**: bcrypt password hashing, rate limiting
- **Database**: Users table với encrypted sensitive fields
- **APIs**: 
  - `POST /api/auth/register`
  - `POST /api/auth/login`
  - `POST /api/auth/logout`
  - `POST /api/auth/forgot-password`
  - `GET /api/auth/social/:provider`

---

### F02: User Profile Management
**Epic**: Personal profile creation và management cho app users

#### User Stories:
- **US02.1**: Tôi muốn tạo profile cá nhân để identify mình trong app
- **US02.2**: Tôi muốn upload avatar để personalize account
- **US02.3**: Tôi muốn edit thông tin cá nhân khi cần update
- **US02.4**: Tôi muốn set privacy preferences để control data visibility

#### Acceptance Criteria:
**AC02.1** - Profile Creation:
- [ ] User nhập họ tên, ngày sinh, giới tính, địa chỉ
- [ ] Phone number optional nhưng có validation format
- [ ] Bio field để describe bản thân (optional)
- [ ] Auto-save draft khi user đang nhập
- [ ] Progress indicator cho profile completion

**AC02.2** - Avatar Upload:
- [ ] Support JPG, PNG files ≤5MB
- [ ] Auto-resize to 400x400px
- [ ] Crop tool để adjust image
- [ ] Default avatar nếu không upload
- [ ] Preview before save

**AC02.3** - Profile Editing:
- [ ] Edit tất cả profile fields
- [ ] Confirmation trước khi save major changes
- [ ] Version history cho important changes
- [ ] Cancel changes option
- [ ] Success/error feedback

**AC02.4** - Privacy Settings:
- [ ] Control profile visibility (public/family/private)
- [ ] Email notification preferences
- [ ] Data sharing preferences
- [ ] Account deletion option
- [ ] Export personal data option

#### Technical Specifications:
- **Database**: User profiles table với JSONB cho flexible fields
- **File Storage**: AWS S3 cho avatars với CDN
- **APIs**:
  - `GET /api/user/profile`
  - `PUT /api/user/profile`
  - `POST /api/user/avatar`
  - `PUT /api/user/settings`

---

### F03: Deceased Profile Creation
**Epic**: Comprehensive profile management cho người đã mất

#### User Stories:
- **US03.1**: Tôi muốn tạo profile cho người thân đã mất để lưu giữ thông tin
- **US03.2**: Tôi muốn nhập thông tin cơ bản (tên, ngày sinh/mất) một cách dễ dàng
- **US03.3**: Tôi muốn thêm ngày cúng đặc biệt để không quên các lễ quan trọng
- **US03.4**: Tôi muốn lưu thông tin nơi an nghỉ để gia đình biết

#### Acceptance Criteria:
**AC03.1** - Basic Information:
- [ ] Họ tên đầy đủ, tên thường gọi
- [ ] Ngày sinh, ngày mất với date picker
- [ ] Nơi sinh, nơi mất với location suggestion
- [ ] Nghề nghiệp, học vấn
- [ ] Nguyên nhân mất (optional, sensitive)

**AC03.2** - Special Dates:
- [ ] Ngày giỗ hàng năm (auto-calculate từ ngày mất)
- [ ] 49 ngày, 100 ngày cúng
- [ ] Các ngày lễ đặc biệt khác
- [ ] Calendar integration để remind
- [ ] Âm lịch/dương lịch options

**AC03.3** - Resting Place:
- [ ] Tên nghĩa trang/chùa
- [ ] Địa chỉ chi tiết
- [ ] Số khu, số mộ
- [ ] GPS coordinates (optional)
- [ ] Photos của nơi an nghỉ

**AC03.4** - Additional Information:
- [ ] Mối quan hệ với user (cha, mẹ, ông, bà...)
- [ ] Brief biography/description
- [ ] Personality traits, hobbies
- [ ] Achievements, memorable quotes
- [ ] Family stories/memories

#### Technical Specifications:
- **Database**: Deceased profiles table với full-text search
- **Validation**: Date validation, required field checking
- **APIs**:
  - `POST /api/profiles`
  - `GET /api/profiles`
  - `PUT /api/profiles/:id`
  - `DELETE /api/profiles/:id`

---

### F04: Media Upload & Gallery
**Epic**: Photo/video management system cho memories preservation

#### User Stories:
- **US04.1**: Tôi muốn upload photos của người thân để preserve memories
- **US04.2**: Tôi muốn organize photos theo albums để dễ tìm kiếm
- **US04.3**: Tôi muốn add captions và tags để remember context
- **US04.4**: Tôi muốn view photos trong beautiful gallery interface

#### Acceptance Criteria:
**AC04.1** - Photo Upload:
- [ ] Drag & drop multiple files
- [ ] Support JPG, PNG, HEIC ≤10MB each
- [ ] Progress indicator cho upload
- [ ] Auto-resize and optimize images
- [ ] Generate thumbnails

**AC04.2** - Video Upload:
- [ ] Support MP4, MOV ≤50MB each
- [ ] Video thumbnail generation
- [ ] Basic compression
- [ ] Duration limit 5 minutes
- [ ] Progress indicator

**AC04.3** - Gallery Management:
- [ ] Create albums/folders
- [ ] Move photos between albums
- [ ] Bulk select and actions
- [ ] Sort by date, name, manual
- [ ] Search by filename, caption

**AC04.4** - Media Metadata:
- [ ] Add captions/descriptions
- [ ] Tag photos with people, events
- [ ] Date taken (from EXIF or manual)
- [ ] Location info (optional)
- [ ] Privacy settings per photo

#### Technical Specifications:
- **Storage**: AWS S3 với CloudFront CDN
- **Processing**: Sharp.js cho image optimization
- **Database**: Media table với metadata JSONB
- **APIs**:
  - `POST /api/profiles/:id/media`
  - `GET /api/profiles/:id/media`
  - `PUT /api/media/:id`
  - `DELETE /api/media/:id`

---

### F05: Basic Family Tree
**Epic**: Simple family relationship visualization và management

#### User Stories:
- **US05.1**: Tôi muốn tạo family tree để show relationships
- **US05.2**: Tôi muốn thêm family members và connect relationships
- **US05.3**: Tôi muốn view family tree dưới dạng visual diagram
- **US05.4**: Tôi muốn edit relationships khi có changes

#### Acceptance Criteria:
**AC05.1** - Add Family Members:
- [ ] Link existing profiles hoặc create new
- [ ] Define relationship types (parent, child, spouse, sibling)
- [ ] Add multiple relationships per person
- [ ] Validate relationship logic (no circular relationships)
- [ ] Support deceased and living members

**AC05.2** - Tree Visualization:
- [ ] Basic tree layout với boxes và connecting lines
- [ ] Show photos và basic info per person
- [ ] Zoom in/out capability
- [ ] Pan around large trees
- [ ] Responsive design cho mobile viewing

**AC05.3** - Relationship Management:
- [ ] Edit existing relationships
- [ ] Delete relationships với confirmation
- [ ] Add relationship notes/details
- [ ] Set relationship dates (marriage, etc.)
- [ ] Mark primary relationships

**AC05.4** - Tree Navigation:
- [ ] Focus on specific person
- [ ] Expand/collapse branches
- [ ] Search for specific person
- [ ] Navigate between generations
- [ ] Export tree as image/PDF

#### Technical Specifications:
- **Database**: Neo4j graph database cho complex relationships
- **Visualization**: D3.js hoặc similar library
- **APIs**:
  - `GET /api/family-tree/:familyId`
  - `POST /api/family-tree/relationships`
  - `PUT /api/family-tree/relationships/:id`
  - `DELETE /api/family-tree/relationships/:id`

---

### F06: Basic Sharing & Privacy
**Epic**: Share profiles với family members và control access

#### User Stories:
- **US06.1**: Tôi muốn invite family members để collaborate trên profiles
- **US06.2**: Tôi muốn control ai có thể xem/edit profile nào
- **US06.3**: Tôi muốn share specific profiles via links
- **US06.4**: Tôi muốn set different privacy levels cho different information

#### Acceptance Criteria:
**AC06.1** - Family Invitations:
- [ ] Invite via email với personalized message
- [ ] Generate invitation links với expiration
- [ ] Accept/decline invitation flow
- [ ] Resend invitations
- [ ] View pending invitations

**AC06.2** - Access Control:
- [ ] Role-based permissions (Admin, Editor, Viewer)
- [ ] Per-profile access control
- [ ] Inheritance of permissions
- [ ] Audit log của access actions
- [ ] Remove access capability

**AC06.3** - Link Sharing:
- [ ] Generate shareable links với passwords
- [ ] Set link expiration dates
- [ ] Control what's visible via links
- [ ] Track link access analytics
- [ ] Disable links anytime

**AC06.4** - Privacy Levels:
- [ ] Public, Family Only, Private options
- [ ] Granular control (basic info, photos, personal details)
- [ ] Default privacy settings
- [ ] Privacy impact warnings
- [ ] Bulk privacy updates

#### Technical Specifications:
- **Authentication**: JWT-based access tokens
- **Database**: Permissions table với role mappings
- **APIs**:
  - `POST /api/profiles/:id/invite`
  - `PUT /api/profiles/:id/permissions`
  - `POST /api/profiles/:id/share`
  - `GET /api/shared/:token`

---

## Phase 2: Should Have Features

### F07: Advanced Family Tree Features
- Interactive timeline view
- Multiple family trees per user
- Import/export GEDCOM files
- Advanced relationship types
- Collaborative editing với conflict resolution

### F08: Calendar & Reminders
- Vietnamese lunar calendar support
- Automated anniversary reminders
- Custom event creation
- Email/SMS notifications
- Integration với popular calendar apps

### F09: Location Management
- Cemetery/temple database
- GPS navigation integration
- Location photos và reviews
- Custom location creation
- Distance calculation

### F10: Basic Service Directory
- Service provider listings
- Contact information
- Basic categories (tang lễ, cúng bái, etc.)
- Search và filter functionality
- Basic rating system

### F11: Memoir Creation Tools
- Rich text editor
- Template system
- Chapter organization
- Photo integration
- Export to PDF/Word

---

## Phase 3: Could Have Features

### F12: Service Marketplace
- Advanced booking system
- Payment integration
- Review và rating system
- Service provider dashboard
- Commission system

### F13: Community Features
- Discussion forums
- Story sharing
- Cultural articles
- Expert advice
- Community events

### F14: Advanced Analytics
- Usage analytics
- Family tree statistics
- Memory engagement metrics
- Trend analysis
- Custom reports

### F15: Mobile App Migration
- React Native app development
- Offline mode capability
- Push notifications
- Camera integration
- GPS features

### F16: Premium Features
- Unlimited storage
- Advanced themes
- Priority support
- Advanced analytics
- White-label options

---

## Technical Constraints & Considerations

### Performance Requirements:
- Page load time <3 seconds
- Image upload <30 seconds for 10MB
- Tree rendering <5 seconds for 100 people
- Search results <2 seconds

### Security Requirements:
- HTTPS everywhere
- Data encryption at rest
- Regular security audits
- GDPR compliance
- Input sanitization

### Scalability Considerations:
- Support 10,000 concurrent users
- Handle 1TB+ of media storage
- Database optimization for large family trees
- CDN for global performance

### Browser Support:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers

---

## Success Metrics & KPIs

### MVP Success Criteria:
- **User Registration**: 1,000 users trong 3 tháng
- **Profile Completion**: 80% users tạo ít nhất 1 deceased profile
- **Content Upload**: 70% users upload ít nhất 5 photos
- **Family Sharing**: 50% users invite ít nhất 1 family member
- **Retention**: 60% users return sau 1 tuần

### Feature-Specific Metrics:
- **Authentication**: <5% abandonment rate during registration
- **Profile Creation**: >80% completion rate for profile wizard
- **Media Upload**: Average 10 photos per deceased profile
- **Family Tree**: Average 8 people per family tree
- **Sharing**: 30% profiles được share with family

### User Experience Metrics:
- **Net Promoter Score**: >7.0
- **App Store Rating**: >4.0 stars
- **Support Tickets**: <5% of users require help
- **Feature Adoption**: >70% of users use core features monthly

---

## Risk Assessment & Mitigation

### Technical Risks:
**Risk**: Complex family relationships causing performance issues  
**Mitigation**: Use graph database, implement caching, progressive loading

**Risk**: Large media files affecting app performance  
**Mitigation**: Image optimization, CDN usage, lazy loading

**Risk**: Data loss during user actions  
**Mitigation**: Auto-save functionality, version control, regular backups

### User Experience Risks:
**Risk**: Elderly users finding interface too complex  
**Mitigation**: Simple UI, large fonts, extensive testing với target users

**Risk**: Privacy concerns limiting adoption  
**Mitigation**: Transparent privacy policy, granular controls, security education

**Risk**: Cultural insensitivity affecting acceptance  
**Mitigation**: Cultural consultant involvement, community feedback loops

### Business Risks:
**Risk**: Low user adoption rates  
**Mitigation**: Extensive beta testing, user feedback integration, marketing strategy

**Risk**: High development costs with small team  
**Mitigation**: MVP-first approach, feature prioritization, efficient tech stack

---

*Feature specifications sẽ được update based on user feedback và development progress. All features subject to technical feasibility assessment và user validation.*