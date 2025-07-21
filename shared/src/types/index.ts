// ==============================================
// Shared Types for Trang Vien So
// ==============================================

import { z } from 'zod';

// ==============================================
// User Management Types
// ==============================================

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  firstName: z.string().min(1).max(100),
  lastName: z.string().min(1).max(100),
  phoneNumber: z.string().optional(),
  avatar: z.string().url().optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type User = z.infer<typeof UserSchema>;

export const AuthRequestSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export type AuthRequest = z.infer<typeof AuthRequestSchema>;

export const RegisterRequestSchema = AuthRequestSchema.extend({
  firstName: z.string().min(1).max(100),
  lastName: z.string().min(1).max(100),
  confirmPassword: z.string().min(8),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

export type RegisterRequest = z.infer<typeof RegisterRequestSchema>;

// ==============================================
// Deceased Profile Types
// ==============================================

export const DeceasedProfileSchema = z.object({
  id: z.string().uuid(),
  firstName: z.string().min(1).max(100),
  lastName: z.string().min(1).max(100),
  dateOfBirth: z.date().optional(),
  dateOfDeath: z.date().optional(),
  placeOfBirth: z.string().max(200).optional(),
  placeOfDeath: z.string().max(200).optional(),
  causeOfDeath: z.string().max(500).optional(),
  biography: z.string().max(5000).optional(),
  
  // Vietnamese-specific fields
  specialDates: z.object({
    deathAnniversary: z.date().optional(), // Ngày giỗ
    worship49Days: z.date().optional(),    // Lễ 49 ngày
    worship100Days: z.date().optional(),   // Lễ 100 ngày
    customDates: z.array(z.object({
      name: z.string(),
      date: z.date(),
      description: z.string().optional(),
    })).optional(),
  }).optional(),
  
  // Location information
  location: z.object({
    cemetery: z.string().max(200).optional(),
    temple: z.string().max(200).optional(),
    customLocation: z.string().max(200).optional(),
    coordinates: z.object({
      lat: z.number(),
      lng: z.number(),
    }).optional(),
  }).optional(),
  
  // Family and access control
  familyId: z.string().uuid().optional(),
  privacyLevel: z.enum(['public', 'family', 'private']).default('family'),
  
  // Metadata
  createdBy: z.string().uuid(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type DeceasedProfile = z.infer<typeof DeceasedProfileSchema>;

export const CreateDeceasedProfileSchema = DeceasedProfileSchema.omit({
  id: true,
  createdBy: true,
  createdAt: true,
  updatedAt: true,
});

export type CreateDeceasedProfileRequest = z.infer<typeof CreateDeceasedProfileSchema>;

// ==============================================
// Media File Types
// ==============================================

export const MediaFileSchema = z.object({
  id: z.string().uuid(),
  profileId: z.string().uuid(),
  fileName: z.string().max(255),
  fileType: z.enum(['image', 'video', 'document']),
  mimeType: z.string().max(100),
  fileSize: z.number().positive(),
  fileUrl: z.string().url(),
  thumbnailUrl: z.string().url().optional(),
  caption: z.string().max(500).optional(),
  uploadedBy: z.string().uuid(),
  createdAt: z.date(),
});

export type MediaFile = z.infer<typeof MediaFileSchema>;

export const UploadMediaRequestSchema = z.object({
  profileId: z.string().uuid(),
  caption: z.string().max(500).optional(),
});

export type UploadMediaRequest = z.infer<typeof UploadMediaRequestSchema>;

// ==============================================
// Family Management Types
// ==============================================

export const FamilyMemberSchema = z.object({
  id: z.string().uuid(),
  familyId: z.string().uuid(),
  userId: z.string().uuid(),
  role: z.enum(['admin', 'editor', 'viewer']),
  invitedBy: z.string().uuid(),
  invitedAt: z.date(),
  joinedAt: z.date().optional(),
  status: z.enum(['pending', 'active', 'inactive']),
});

export type FamilyMember = z.infer<typeof FamilyMemberSchema>;

export const InviteFamilyMemberSchema = z.object({
  email: z.string().email(),
  role: z.enum(['editor', 'viewer']).default('viewer'),
  message: z.string().max(500).optional(),
});

export type InviteFamilyMemberRequest = z.infer<typeof InviteFamilyMemberSchema>;

// ==============================================
// API Response Types
// ==============================================

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: string[];
}

export interface PaginatedResponse<T = any> {
  success: boolean;
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// ==============================================
// Error Types
// ==============================================

export interface ApiError {
  code: string;
  message: string;
  field?: string;
  details?: any;
}

export class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public field?: string,
    public details?: any
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// ==============================================
// Utility Types
// ==============================================

export type Partial<T> = {
  [P in keyof T]?: T[P];
};

export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

export type WithTimestamps<T> = T & {
  createdAt: Date;
  updatedAt: Date;
};

// ==============================================
// Constants
// ==============================================

export const PRIVACY_LEVELS = ['public', 'family', 'private'] as const;
export const FAMILY_ROLES = ['admin', 'editor', 'viewer'] as const;
export const MEDIA_TYPES = ['image', 'video', 'document'] as const;
export const MEMBER_STATUS = ['pending', 'active', 'inactive'] as const;

// File upload limits
export const FILE_UPLOAD_LIMITS = {
  IMAGE_MAX_SIZE: 10 * 1024 * 1024, // 10MB
  VIDEO_MAX_SIZE: 100 * 1024 * 1024, // 100MB
  DOCUMENT_MAX_SIZE: 20 * 1024 * 1024, // 20MB
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/webp'],
  ALLOWED_VIDEO_TYPES: ['video/mp4', 'video/webm'],
  ALLOWED_DOCUMENT_TYPES: ['application/pdf', 'text/plain'],
} as const;

// Vietnamese lunar calendar utilities
export const VIETNAMESE_MONTHS = [
  'Tháng Giêng', 'Tháng Hai', 'Tháng Ba', 'Tháng Tư',
  'Tháng Năm', 'Tháng Sáu', 'Tháng Bảy', 'Tháng Tám',
  'Tháng Chín', 'Tháng Mười', 'Tháng Mười Một', 'Tháng Chạp'
] as const;