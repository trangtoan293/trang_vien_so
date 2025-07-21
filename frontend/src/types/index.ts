// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  message: string
  data?: T
  error?: string
}

// User Types
export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  phone_number?: string
  avatar?: string
  email_verified: boolean
  email_verified_at?: string
  language: string
  timezone: string
  notification_preferences: NotificationPreferences
  privacy_settings: PrivacySettings
  created_at: string
  updated_at: string
  last_login_at?: string
}

export interface NotificationPreferences {
  email: boolean
  push: boolean
  sms?: boolean
  memorial_reminders?: boolean
  family_updates?: boolean
}

export interface PrivacySettings {
  profile_visibility: 'public' | 'family' | 'private'
  allow_search?: boolean
  show_last_login?: boolean
}

// Authentication Types
export interface LoginRequest {
  email: string
  password: string
  remember_me?: boolean
}

export interface RegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
  phone_number?: string
  language?: string
  timezone?: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  expires_at: string
}

export interface LoginResponse {
  success: boolean
  message: string
  user: User
  tokens: AuthTokens
  session_id: string
}

// Deceased Profile Types
export interface DeceasedProfile {
  id: string
  family_id?: string
  created_by: string
  
  // Names - Vietnamese cultural support
  vietnamese_name: string
  english_name?: string
  common_name?: string
  generation_name?: string
  ancestral_title?: string
  
  // Basic information
  gender: string
  
  // Dates - both solar and lunar calendar support
  birth_date?: string
  death_date?: string
  birth_date_lunar?: string
  death_date_lunar?: string
  
  // Places
  birth_place?: string
  death_place?: string
  resting_place?: string
  
  // Personal information
  occupation?: string
  education?: string
  biography?: string
  
  // Vietnamese cultural specific
  special_dates?: Record<string, any>
  cultural_info?: Record<string, any>
  
  // Privacy
  privacy_level: 'public' | 'family' | 'private'
  
  // Media
  profile_photo?: string
  cover_photo?: string
  
  // Timestamps
  created_at: string
  updated_at: string
}

export interface DeceasedProfileCreate {
  family_id?: string
  vietnamese_name: string
  english_name?: string
  common_name?: string
  generation_name?: string
  ancestral_title?: string
  gender: string
  birth_date?: string
  death_date?: string
  birth_date_lunar?: string
  death_date_lunar?: string
  birth_place?: string
  death_place?: string
  resting_place?: string
  occupation?: string
  education?: string
  biography?: string
  special_dates?: Record<string, any>
  cultural_info?: Record<string, any>
  privacy_level: 'public' | 'family' | 'private'
}

export interface DeceasedProfileUpdate {
  vietnamese_name?: string
  english_name?: string
  common_name?: string
  generation_name?: string
  ancestral_title?: string
  gender?: string
  birth_date?: string
  death_date?: string
  birth_date_lunar?: string
  death_date_lunar?: string
  birth_place?: string
  death_place?: string
  resting_place?: string
  occupation?: string
  education?: string
  biography?: string
  special_dates?: Record<string, any>
  cultural_info?: Record<string, any>
  privacy_level?: 'public' | 'family' | 'private'
}

export interface DeceasedProfileList {
  profiles: DeceasedProfile[]
  total: number
  skip: number
  limit: number
}

// Family Types
export interface Family {
  id: string
  name: string
  description?: string
  created_by: string
  created_at: string
  updated_at: string
}

export interface FamilyMember {
  id: string
  family_id: string
  user_id: string
  role: 'admin' | 'member' | 'viewer'
  joined_at: string
  invited_by: string
}

// Media Types
export interface MediaFile {
  id: string
  filename: string
  original_filename: string
  mime_type: string
  size: number
  url: string
  thumbnail_url?: string
  profile_id?: string
  uploaded_by: string
  uploaded_at: string
}

// Vietnamese Cultural Types
export interface LunarDate {
  day: number
  month: number
  year: number
  is_leap_month?: boolean
}

export interface SpecialDate {
  name: string
  date: string
  lunar_date?: LunarDate
  description?: string
  type: 'birthday' | 'death_anniversary' | 'memorial_day' | 'festival' | 'other'
}

export interface CulturalInfo {
  religion?: string
  hometown?: string
  clan_name?: string
  burial_traditions?: string[]
  memorial_traditions?: string[]
  special_customs?: string
}

// Form Types
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'textarea' | 'select' | 'date' | 'file'
  placeholder?: string
  required?: boolean
  options?: Array<{ value: string; label: string }>
}

// UI Types
export interface NavigationItem {
  name: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
  current?: boolean
  children?: NavigationItem[]
}

export interface BreadcrumbItem {
  name: string
  href?: string
  current?: boolean
}

// Error Types
export interface AppError {
  code: string
  message: string
  details?: Record<string, any>
}

// Loading States
export interface LoadingState {
  loading: boolean
  error?: string | null
}

// Pagination
export interface PaginationParams {
  page: number
  limit: number
  total?: number
}

// Search
export interface SearchParams {
  query?: string
  filters?: Record<string, any>
  sort?: string
  order?: 'asc' | 'desc'
}

// Environment Variables
declare global {
  interface ImportMetaEnv {
    readonly VITE_API_URL: string
    readonly VITE_APP_NAME: string
    readonly VITE_APP_VERSION: string
    readonly VITE_ENVIRONMENT: string
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}