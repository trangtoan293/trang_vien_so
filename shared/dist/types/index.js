"use strict";
// ==============================================
// Shared Types for Trang Vien So
// ==============================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.VIETNAMESE_MONTHS = exports.FILE_UPLOAD_LIMITS = exports.MEMBER_STATUS = exports.MEDIA_TYPES = exports.FAMILY_ROLES = exports.PRIVACY_LEVELS = exports.AppError = exports.InviteFamilyMemberSchema = exports.FamilyMemberSchema = exports.UploadMediaRequestSchema = exports.MediaFileSchema = exports.CreateDeceasedProfileSchema = exports.DeceasedProfileSchema = exports.RegisterRequestSchema = exports.AuthRequestSchema = exports.UserSchema = void 0;
const zod_1 = require("zod");
// ==============================================
// User Management Types
// ==============================================
exports.UserSchema = zod_1.z.object({
    id: zod_1.z.string().uuid(),
    email: zod_1.z.string().email(),
    firstName: zod_1.z.string().min(1).max(100),
    lastName: zod_1.z.string().min(1).max(100),
    phoneNumber: zod_1.z.string().optional(),
    avatar: zod_1.z.string().url().optional(),
    createdAt: zod_1.z.date(),
    updatedAt: zod_1.z.date(),
});
exports.AuthRequestSchema = zod_1.z.object({
    email: zod_1.z.string().email(),
    password: zod_1.z.string().min(8),
});
exports.RegisterRequestSchema = exports.AuthRequestSchema.extend({
    firstName: zod_1.z.string().min(1).max(100),
    lastName: zod_1.z.string().min(1).max(100),
    confirmPassword: zod_1.z.string().min(8),
}).refine(data => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
});
// ==============================================
// Deceased Profile Types
// ==============================================
exports.DeceasedProfileSchema = zod_1.z.object({
    id: zod_1.z.string().uuid(),
    firstName: zod_1.z.string().min(1).max(100),
    lastName: zod_1.z.string().min(1).max(100),
    dateOfBirth: zod_1.z.date().optional(),
    dateOfDeath: zod_1.z.date().optional(),
    placeOfBirth: zod_1.z.string().max(200).optional(),
    placeOfDeath: zod_1.z.string().max(200).optional(),
    causeOfDeath: zod_1.z.string().max(500).optional(),
    biography: zod_1.z.string().max(5000).optional(),
    // Vietnamese-specific fields
    specialDates: zod_1.z.object({
        deathAnniversary: zod_1.z.date().optional(), // Ngày giỗ
        worship49Days: zod_1.z.date().optional(), // Lễ 49 ngày
        worship100Days: zod_1.z.date().optional(), // Lễ 100 ngày
        customDates: zod_1.z.array(zod_1.z.object({
            name: zod_1.z.string(),
            date: zod_1.z.date(),
            description: zod_1.z.string().optional(),
        })).optional(),
    }).optional(),
    // Location information
    location: zod_1.z.object({
        cemetery: zod_1.z.string().max(200).optional(),
        temple: zod_1.z.string().max(200).optional(),
        customLocation: zod_1.z.string().max(200).optional(),
        coordinates: zod_1.z.object({
            lat: zod_1.z.number(),
            lng: zod_1.z.number(),
        }).optional(),
    }).optional(),
    // Family and access control
    familyId: zod_1.z.string().uuid().optional(),
    privacyLevel: zod_1.z.enum(['public', 'family', 'private']).default('family'),
    // Metadata
    createdBy: zod_1.z.string().uuid(),
    createdAt: zod_1.z.date(),
    updatedAt: zod_1.z.date(),
});
exports.CreateDeceasedProfileSchema = exports.DeceasedProfileSchema.omit({
    id: true,
    createdBy: true,
    createdAt: true,
    updatedAt: true,
});
// ==============================================
// Media File Types
// ==============================================
exports.MediaFileSchema = zod_1.z.object({
    id: zod_1.z.string().uuid(),
    profileId: zod_1.z.string().uuid(),
    fileName: zod_1.z.string().max(255),
    fileType: zod_1.z.enum(['image', 'video', 'document']),
    mimeType: zod_1.z.string().max(100),
    fileSize: zod_1.z.number().positive(),
    fileUrl: zod_1.z.string().url(),
    thumbnailUrl: zod_1.z.string().url().optional(),
    caption: zod_1.z.string().max(500).optional(),
    uploadedBy: zod_1.z.string().uuid(),
    createdAt: zod_1.z.date(),
});
exports.UploadMediaRequestSchema = zod_1.z.object({
    profileId: zod_1.z.string().uuid(),
    caption: zod_1.z.string().max(500).optional(),
});
// ==============================================
// Family Management Types
// ==============================================
exports.FamilyMemberSchema = zod_1.z.object({
    id: zod_1.z.string().uuid(),
    familyId: zod_1.z.string().uuid(),
    userId: zod_1.z.string().uuid(),
    role: zod_1.z.enum(['admin', 'editor', 'viewer']),
    invitedBy: zod_1.z.string().uuid(),
    invitedAt: zod_1.z.date(),
    joinedAt: zod_1.z.date().optional(),
    status: zod_1.z.enum(['pending', 'active', 'inactive']),
});
exports.InviteFamilyMemberSchema = zod_1.z.object({
    email: zod_1.z.string().email(),
    role: zod_1.z.enum(['editor', 'viewer']).default('viewer'),
    message: zod_1.z.string().max(500).optional(),
});
class AppError extends Error {
    constructor(statusCode, code, message, field, details) {
        super(message);
        this.statusCode = statusCode;
        this.code = code;
        this.field = field;
        this.details = details;
        this.name = 'AppError';
    }
}
exports.AppError = AppError;
// ==============================================
// Constants
// ==============================================
exports.PRIVACY_LEVELS = ['public', 'family', 'private'];
exports.FAMILY_ROLES = ['admin', 'editor', 'viewer'];
exports.MEDIA_TYPES = ['image', 'video', 'document'];
exports.MEMBER_STATUS = ['pending', 'active', 'inactive'];
// File upload limits
exports.FILE_UPLOAD_LIMITS = {
    IMAGE_MAX_SIZE: 10 * 1024 * 1024, // 10MB
    VIDEO_MAX_SIZE: 100 * 1024 * 1024, // 100MB
    DOCUMENT_MAX_SIZE: 20 * 1024 * 1024, // 20MB
    ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/webp'],
    ALLOWED_VIDEO_TYPES: ['video/mp4', 'video/webm'],
    ALLOWED_DOCUMENT_TYPES: ['application/pdf', 'text/plain'],
};
// Vietnamese lunar calendar utilities
exports.VIETNAMESE_MONTHS = [
    'Tháng Giêng', 'Tháng Hai', 'Tháng Ba', 'Tháng Tư',
    'Tháng Năm', 'Tháng Sáu', 'Tháng Bảy', 'Tháng Tám',
    'Tháng Chín', 'Tháng Mười', 'Tháng Mười Một', 'Tháng Chạp'
];
//# sourceMappingURL=index.js.map