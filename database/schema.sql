-- ==============================================
-- Trang Vien So Database Schema
-- Vietnamese Memorial App Database Structure
-- ==============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For full-text search

-- ==============================================
-- Users Table
-- ==============================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    avatar VARCHAR(500), -- URL to avatar image
    email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    
    -- Settings
    language VARCHAR(10) DEFAULT 'vi',
    timezone VARCHAR(50) DEFAULT 'Asia/Ho_Chi_Minh',
    notification_preferences JSONB DEFAULT '{"email": true, "push": true}',
    privacy_settings JSONB DEFAULT '{"profile_visibility": "family"}',
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    
    -- Constraints
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    CONSTRAINT name_length CHECK (LENGTH(first_name) > 0 AND LENGTH(last_name) > 0)
);

-- ==============================================
-- Families Table
-- ==============================================
CREATE TABLE families (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    family_name VARCHAR(200) NOT NULL,
    description TEXT,
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ==============================================
-- Family Members Table
-- ==============================================
CREATE TABLE family_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    family_id UUID NOT NULL REFERENCES families(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'editor', 'viewer')),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'inactive')),
    invited_by UUID NOT NULL REFERENCES users(id),
    invited_at TIMESTAMP DEFAULT NOW(),
    joined_at TIMESTAMP,
    
    -- Constraints
    UNIQUE(family_id, user_id)
);

-- ==============================================
-- Deceased Profiles Table
-- ==============================================
CREATE TABLE deceased_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Basic Information
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    nickname VARCHAR(100),
    
    -- Life Dates
    date_of_birth DATE,
    date_of_death DATE,
    place_of_birth VARCHAR(200),
    place_of_death VARCHAR(200),
    cause_of_death VARCHAR(500),
    
    -- Biography
    biography TEXT,
    life_achievements TEXT,
    memorable_quotes TEXT,
    
    -- Vietnamese Specific Fields
    special_dates JSONB DEFAULT '{}', -- Ngày giỗ, lễ 49 ngày, 100 ngày, etc.
    vietnamese_name VARCHAR(200), -- Tên tiếng Việt
    generation_name VARCHAR(100), -- Tên thế hệ
    ancestral_title VARCHAR(200), -- Hiệu
    
    -- Location Information
    location_info JSONB DEFAULT '{}', -- Cemetery, temple, coordinates
    
    -- Family & Access Control
    family_id UUID REFERENCES families(id),
    privacy_level VARCHAR(20) DEFAULT 'family' CHECK (privacy_level IN ('public', 'family', 'private')),
    allowed_users UUID[] DEFAULT '{}', -- Specific users who can access if privacy_level = 'private'
    
    -- Media
    profile_photo VARCHAR(500), -- Main profile photo URL
    cover_photo VARCHAR(500), -- Cover/banner photo URL
    
    -- Metadata
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_modified_by UUID REFERENCES users(id),
    view_count INTEGER DEFAULT 0,
    
    -- Search optimization
    search_vector tsvector,
    
    -- Constraints
    CONSTRAINT valid_dates CHECK (date_of_death IS NULL OR date_of_birth IS NULL OR date_of_death >= date_of_birth),
    CONSTRAINT name_required CHECK (LENGTH(first_name) > 0 AND LENGTH(last_name) > 0)
);

-- ==============================================
-- Media Files Table
-- ==============================================
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id UUID NOT NULL REFERENCES deceased_profiles(id) ON DELETE CASCADE,
    
    -- File Information
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    
    -- File Metadata
    file_type VARCHAR(50) NOT NULL CHECK (file_type IN ('image', 'video', 'document', 'audio')),
    mime_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL CHECK (file_size > 0),
    width INTEGER, -- For images/videos
    height INTEGER, -- For images/videos
    duration INTEGER, -- For videos/audio (in seconds)
    
    -- Content Information
    caption TEXT,
    description TEXT,
    tags VARCHAR(500)[], -- Array of tags
    date_taken TIMESTAMP, -- When the photo/video was taken
    location_taken VARCHAR(200), -- Where the photo/video was taken
    
    -- Upload Information
    uploaded_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Display Order
    display_order INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE -- Featured in profile
);

-- ==============================================
-- Invitations Table
-- ==============================================
CREATE TABLE invitations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL,
    family_id UUID NOT NULL REFERENCES families(id) ON DELETE CASCADE,
    invited_by UUID NOT NULL REFERENCES users(id),
    role VARCHAR(20) NOT NULL CHECK (role IN ('editor', 'viewer')),
    token VARCHAR(255) UNIQUE NOT NULL,
    message TEXT,
    
    -- Status tracking
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'expired')),
    expires_at TIMESTAMP NOT NULL,
    accepted_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- ==============================================
-- Activity Log Table
-- ==============================================
CREATE TABLE activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    profile_id UUID REFERENCES deceased_profiles(id),
    family_id UUID REFERENCES families(id),
    
    -- Activity details
    action VARCHAR(100) NOT NULL, -- 'created', 'updated', 'deleted', 'viewed', etc.
    entity_type VARCHAR(50) NOT NULL, -- 'profile', 'media', 'family', etc.
    entity_id UUID,
    
    -- Change details
    changes JSONB, -- What was changed
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Index for performance
    INDEX idx_activity_logs_user_created (user_id, created_at),
    INDEX idx_activity_logs_profile_created (profile_id, created_at)
);

-- ==============================================
-- Sessions Table (for JWT token management)
-- ==============================================
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    refresh_token_hash VARCHAR(255),
    
    -- Session metadata
    ip_address INET,
    user_agent TEXT,
    device_info JSONB,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    last_used_at TIMESTAMP DEFAULT NOW(),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Constraints
    UNIQUE(token_hash)
);

-- ==============================================
-- Indexes for Performance
-- ==============================================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Deceased profiles indexes
CREATE INDEX idx_deceased_profiles_family_id ON deceased_profiles(family_id);
CREATE INDEX idx_deceased_profiles_created_by ON deceased_profiles(created_by);
CREATE INDEX idx_deceased_profiles_privacy ON deceased_profiles(privacy_level);
CREATE INDEX idx_deceased_profiles_search ON deceased_profiles USING gin(search_vector);
CREATE INDEX idx_deceased_profiles_dates ON deceased_profiles(date_of_birth, date_of_death);

-- Media files indexes
CREATE INDEX idx_media_files_profile_id ON media_files(profile_id);
CREATE INDEX idx_media_files_type ON media_files(file_type);
CREATE INDEX idx_media_files_created ON media_files(created_at);
CREATE INDEX idx_media_files_featured ON media_files(is_featured) WHERE is_featured = TRUE;

-- Family members indexes
CREATE INDEX idx_family_members_family_id ON family_members(family_id);
CREATE INDEX idx_family_members_user_id ON family_members(user_id);
CREATE INDEX idx_family_members_status ON family_members(status);

-- Invitations indexes
CREATE INDEX idx_invitations_email ON invitations(email);
CREATE INDEX idx_invitations_token ON invitations(token);
CREATE INDEX idx_invitations_expires ON invitations(expires_at);
CREATE INDEX idx_invitations_status ON invitations(status);

-- Sessions indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);
CREATE INDEX idx_user_sessions_active ON user_sessions(is_active) WHERE is_active = TRUE;

-- ==============================================
-- Full-Text Search Configuration
-- ==============================================

-- Function to update search vector
CREATE OR REPLACE FUNCTION update_deceased_profile_search_vector() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('simple', COALESCE(NEW.first_name, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.last_name, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.middle_name, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(NEW.nickname, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(NEW.vietnamese_name, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.biography, '')), 'C') ||
        setweight(to_tsvector('simple', COALESCE(NEW.place_of_birth, '')), 'D') ||
        setweight(to_tsvector('simple', COALESCE(NEW.place_of_death, '')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update search vector
CREATE TRIGGER update_deceased_profile_search_vector_trigger
    BEFORE INSERT OR UPDATE ON deceased_profiles
    FOR EACH ROW EXECUTE FUNCTION update_deceased_profile_search_vector();

-- ==============================================
-- Triggers for Updated At
-- ==============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_deceased_profiles_updated_at BEFORE UPDATE ON deceased_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_families_updated_at BEFORE UPDATE ON families
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_media_files_updated_at BEFORE UPDATE ON media_files
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================
-- Views for Common Queries
-- ==============================================

-- View for profile with creator information
CREATE VIEW profiles_with_creator AS
SELECT 
    p.*,
    u.first_name as creator_first_name,
    u.last_name as creator_last_name,
    u.email as creator_email,
    f.family_name
FROM deceased_profiles p
LEFT JOIN users u ON p.created_by = u.id
LEFT JOIN families f ON p.family_id = f.id;

-- View for media with profile information
CREATE VIEW media_with_profile AS
SELECT 
    m.*,
    p.first_name as profile_first_name,
    p.last_name as profile_last_name,
    p.family_id
FROM media_files m
JOIN deceased_profiles p ON m.profile_id = p.id;

-- ==============================================
-- Sample Data (for development/testing)
-- ==============================================

-- Insert sample family
INSERT INTO families (id, family_name, created_by) VALUES 
('00000000-0000-0000-0000-000000000001', 'Gia đình Nguyễn', '00000000-0000-0000-0000-000000000001');

-- Note: User and profile sample data will be inserted via application seed scripts
-- to ensure proper password hashing and validation

-- ==============================================
-- Database Functions and Procedures
-- ==============================================

-- Function to get family tree data (basic version)
CREATE OR REPLACE FUNCTION get_family_profiles(family_uuid UUID)
RETURNS TABLE (
    profile_id UUID,
    full_name TEXT,
    date_of_birth DATE,
    date_of_death DATE,
    profile_photo VARCHAR(500),
    relationship_level INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        CONCAT(p.first_name, ' ', p.last_name),
        p.date_of_birth,
        p.date_of_death,
        p.profile_photo,
        1 as relationship_level -- Basic implementation, can be enhanced later
    FROM deceased_profiles p
    WHERE p.family_id = family_uuid
    ORDER BY p.date_of_birth NULLS LAST;
END;
$$ LANGUAGE plpgsql;

-- Function to cleanup expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM user_sessions 
    WHERE expires_at < NOW() OR is_active = FALSE;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to cleanup expired invitations
CREATE OR REPLACE FUNCTION cleanup_expired_invitations()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    UPDATE invitations 
    SET status = 'expired' 
    WHERE expires_at < NOW() AND status = 'pending';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- ==============================================
-- Row Level Security (RLS) Setup
-- ==============================================

-- Enable RLS on sensitive tables
ALTER TABLE deceased_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE media_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE family_members ENABLE ROW LEVEL SECURITY;

-- Policies for deceased_profiles
CREATE POLICY "Users can view profiles they have access to" ON deceased_profiles
    FOR SELECT USING (
        privacy_level = 'public' OR
        created_by = current_setting('app.user_id')::UUID OR
        family_id IN (
            SELECT family_id FROM family_members 
            WHERE user_id = current_setting('app.user_id')::UUID 
            AND status = 'active'
        ) OR
        current_setting('app.user_id')::UUID = ANY(allowed_users)
    );

CREATE POLICY "Users can edit profiles they created or have permission to" ON deceased_profiles
    FOR ALL USING (
        created_by = current_setting('app.user_id')::UUID OR
        family_id IN (
            SELECT family_id FROM family_members 
            WHERE user_id = current_setting('app.user_id')::UUID 
            AND status = 'active'
            AND role IN ('admin', 'editor')
        )
    );

-- ==============================================
-- Performance Optimization
-- ==============================================

-- Partial indexes for common queries
CREATE INDEX idx_deceased_profiles_public ON deceased_profiles(created_at) 
    WHERE privacy_level = 'public';

CREATE INDEX idx_active_family_members ON family_members(family_id, user_id) 
    WHERE status = 'active';

-- ==============================================
-- Comments for Documentation
-- ==============================================

COMMENT ON TABLE users IS 'User accounts and authentication information';
COMMENT ON TABLE families IS 'Family groups that can share profiles';
COMMENT ON TABLE deceased_profiles IS 'Memorial profiles for deceased family members';
COMMENT ON TABLE media_files IS 'Photos, videos, and documents associated with profiles';
COMMENT ON TABLE family_members IS 'Users who belong to families with specific roles';
COMMENT ON TABLE invitations IS 'Email invitations to join families';
COMMENT ON TABLE activity_logs IS 'Audit trail of user actions';
COMMENT ON TABLE user_sessions IS 'Active user sessions for JWT token management';

COMMENT ON COLUMN deceased_profiles.special_dates IS 'JSON object containing Vietnamese worship dates and custom commemoration dates';
COMMENT ON COLUMN deceased_profiles.location_info IS 'JSON object containing cemetery, temple, and GPS coordinates';
COMMENT ON COLUMN deceased_profiles.search_vector IS 'Full-text search vector for name and biography content';