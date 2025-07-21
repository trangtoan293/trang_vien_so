import { z } from 'zod';
export declare const UserSchema: z.ZodObject<{
    id: z.ZodString;
    email: z.ZodString;
    firstName: z.ZodString;
    lastName: z.ZodString;
    phoneNumber: z.ZodOptional<z.ZodString>;
    avatar: z.ZodOptional<z.ZodString>;
    createdAt: z.ZodDate;
    updatedAt: z.ZodDate;
}, "strip", z.ZodTypeAny, {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    createdAt: Date;
    updatedAt: Date;
    phoneNumber?: string | undefined;
    avatar?: string | undefined;
}, {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    createdAt: Date;
    updatedAt: Date;
    phoneNumber?: string | undefined;
    avatar?: string | undefined;
}>;
export type User = z.infer<typeof UserSchema>;
export declare const AuthRequestSchema: z.ZodObject<{
    email: z.ZodString;
    password: z.ZodString;
}, "strip", z.ZodTypeAny, {
    email: string;
    password: string;
}, {
    email: string;
    password: string;
}>;
export type AuthRequest = z.infer<typeof AuthRequestSchema>;
export declare const RegisterRequestSchema: z.ZodEffects<z.ZodObject<{
    email: z.ZodString;
    password: z.ZodString;
} & {
    firstName: z.ZodString;
    lastName: z.ZodString;
    confirmPassword: z.ZodString;
}, "strip", z.ZodTypeAny, {
    email: string;
    password: string;
    confirmPassword: string;
    firstName: string;
    lastName: string;
}, {
    email: string;
    password: string;
    confirmPassword: string;
    firstName: string;
    lastName: string;
}>, {
    email: string;
    password: string;
    confirmPassword: string;
    firstName: string;
    lastName: string;
}, {
    email: string;
    password: string;
    confirmPassword: string;
    firstName: string;
    lastName: string;
}>;
export type RegisterRequest = z.infer<typeof RegisterRequestSchema>;
export declare const DeceasedProfileSchema: z.ZodObject<{
    id: z.ZodString;
    firstName: z.ZodString;
    lastName: z.ZodString;
    dateOfBirth: z.ZodOptional<z.ZodDate>;
    dateOfDeath: z.ZodOptional<z.ZodDate>;
    placeOfBirth: z.ZodOptional<z.ZodString>;
    placeOfDeath: z.ZodOptional<z.ZodString>;
    causeOfDeath: z.ZodOptional<z.ZodString>;
    biography: z.ZodOptional<z.ZodString>;
    specialDates: z.ZodOptional<z.ZodObject<{
        deathAnniversary: z.ZodOptional<z.ZodDate>;
        worship49Days: z.ZodOptional<z.ZodDate>;
        worship100Days: z.ZodOptional<z.ZodDate>;
        customDates: z.ZodOptional<z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            date: z.ZodDate;
            description: z.ZodOptional<z.ZodString>;
        }, "strip", z.ZodTypeAny, {
            date: Date;
            name: string;
            description?: string | undefined;
        }, {
            date: Date;
            name: string;
            description?: string | undefined;
        }>, "many">>;
    }, "strip", z.ZodTypeAny, {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    }, {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    }>>;
    location: z.ZodOptional<z.ZodObject<{
        cemetery: z.ZodOptional<z.ZodString>;
        temple: z.ZodOptional<z.ZodString>;
        customLocation: z.ZodOptional<z.ZodString>;
        coordinates: z.ZodOptional<z.ZodObject<{
            lat: z.ZodNumber;
            lng: z.ZodNumber;
        }, "strip", z.ZodTypeAny, {
            lat: number;
            lng: number;
        }, {
            lat: number;
            lng: number;
        }>>;
    }, "strip", z.ZodTypeAny, {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    }, {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    }>>;
    familyId: z.ZodOptional<z.ZodString>;
    privacyLevel: z.ZodDefault<z.ZodEnum<["public", "family", "private"]>>;
    createdBy: z.ZodString;
    createdAt: z.ZodDate;
    updatedAt: z.ZodDate;
}, "strip", z.ZodTypeAny, {
    id: string;
    firstName: string;
    lastName: string;
    createdAt: Date;
    updatedAt: Date;
    privacyLevel: "public" | "private" | "family";
    createdBy: string;
    familyId?: string | undefined;
    dateOfBirth?: Date | undefined;
    dateOfDeath?: Date | undefined;
    placeOfBirth?: string | undefined;
    placeOfDeath?: string | undefined;
    causeOfDeath?: string | undefined;
    biography?: string | undefined;
    specialDates?: {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    } | undefined;
    location?: {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    } | undefined;
}, {
    id: string;
    firstName: string;
    lastName: string;
    createdAt: Date;
    updatedAt: Date;
    createdBy: string;
    familyId?: string | undefined;
    dateOfBirth?: Date | undefined;
    dateOfDeath?: Date | undefined;
    placeOfBirth?: string | undefined;
    placeOfDeath?: string | undefined;
    causeOfDeath?: string | undefined;
    biography?: string | undefined;
    specialDates?: {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    } | undefined;
    location?: {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    } | undefined;
    privacyLevel?: "public" | "private" | "family" | undefined;
}>;
export type DeceasedProfile = z.infer<typeof DeceasedProfileSchema>;
export declare const CreateDeceasedProfileSchema: z.ZodObject<globalThis.Omit<{
    id: z.ZodString;
    firstName: z.ZodString;
    lastName: z.ZodString;
    dateOfBirth: z.ZodOptional<z.ZodDate>;
    dateOfDeath: z.ZodOptional<z.ZodDate>;
    placeOfBirth: z.ZodOptional<z.ZodString>;
    placeOfDeath: z.ZodOptional<z.ZodString>;
    causeOfDeath: z.ZodOptional<z.ZodString>;
    biography: z.ZodOptional<z.ZodString>;
    specialDates: z.ZodOptional<z.ZodObject<{
        deathAnniversary: z.ZodOptional<z.ZodDate>;
        worship49Days: z.ZodOptional<z.ZodDate>;
        worship100Days: z.ZodOptional<z.ZodDate>;
        customDates: z.ZodOptional<z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            date: z.ZodDate;
            description: z.ZodOptional<z.ZodString>;
        }, "strip", z.ZodTypeAny, {
            date: Date;
            name: string;
            description?: string | undefined;
        }, {
            date: Date;
            name: string;
            description?: string | undefined;
        }>, "many">>;
    }, "strip", z.ZodTypeAny, {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    }, {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    }>>;
    location: z.ZodOptional<z.ZodObject<{
        cemetery: z.ZodOptional<z.ZodString>;
        temple: z.ZodOptional<z.ZodString>;
        customLocation: z.ZodOptional<z.ZodString>;
        coordinates: z.ZodOptional<z.ZodObject<{
            lat: z.ZodNumber;
            lng: z.ZodNumber;
        }, "strip", z.ZodTypeAny, {
            lat: number;
            lng: number;
        }, {
            lat: number;
            lng: number;
        }>>;
    }, "strip", z.ZodTypeAny, {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    }, {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    }>>;
    familyId: z.ZodOptional<z.ZodString>;
    privacyLevel: z.ZodDefault<z.ZodEnum<["public", "family", "private"]>>;
    createdBy: z.ZodString;
    createdAt: z.ZodDate;
    updatedAt: z.ZodDate;
}, "id" | "createdAt" | "updatedAt" | "createdBy">, "strip", z.ZodTypeAny, {
    firstName: string;
    lastName: string;
    privacyLevel: "public" | "private" | "family";
    familyId?: string | undefined;
    dateOfBirth?: Date | undefined;
    dateOfDeath?: Date | undefined;
    placeOfBirth?: string | undefined;
    placeOfDeath?: string | undefined;
    causeOfDeath?: string | undefined;
    biography?: string | undefined;
    specialDates?: {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    } | undefined;
    location?: {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    } | undefined;
}, {
    firstName: string;
    lastName: string;
    familyId?: string | undefined;
    dateOfBirth?: Date | undefined;
    dateOfDeath?: Date | undefined;
    placeOfBirth?: string | undefined;
    placeOfDeath?: string | undefined;
    causeOfDeath?: string | undefined;
    biography?: string | undefined;
    specialDates?: {
        deathAnniversary?: Date | undefined;
        worship49Days?: Date | undefined;
        worship100Days?: Date | undefined;
        customDates?: {
            date: Date;
            name: string;
            description?: string | undefined;
        }[] | undefined;
    } | undefined;
    location?: {
        cemetery?: string | undefined;
        temple?: string | undefined;
        customLocation?: string | undefined;
        coordinates?: {
            lat: number;
            lng: number;
        } | undefined;
    } | undefined;
    privacyLevel?: "public" | "private" | "family" | undefined;
}>;
export type CreateDeceasedProfileRequest = z.infer<typeof CreateDeceasedProfileSchema>;
export declare const MediaFileSchema: z.ZodObject<{
    id: z.ZodString;
    profileId: z.ZodString;
    fileName: z.ZodString;
    fileType: z.ZodEnum<["image", "video", "document"]>;
    mimeType: z.ZodString;
    fileSize: z.ZodNumber;
    fileUrl: z.ZodString;
    thumbnailUrl: z.ZodOptional<z.ZodString>;
    caption: z.ZodOptional<z.ZodString>;
    uploadedBy: z.ZodString;
    createdAt: z.ZodDate;
}, "strip", z.ZodTypeAny, {
    profileId: string;
    id: string;
    createdAt: Date;
    fileName: string;
    fileType: "image" | "video" | "document";
    mimeType: string;
    fileSize: number;
    fileUrl: string;
    uploadedBy: string;
    thumbnailUrl?: string | undefined;
    caption?: string | undefined;
}, {
    profileId: string;
    id: string;
    createdAt: Date;
    fileName: string;
    fileType: "image" | "video" | "document";
    mimeType: string;
    fileSize: number;
    fileUrl: string;
    uploadedBy: string;
    thumbnailUrl?: string | undefined;
    caption?: string | undefined;
}>;
export type MediaFile = z.infer<typeof MediaFileSchema>;
export declare const UploadMediaRequestSchema: z.ZodObject<{
    profileId: z.ZodString;
    caption: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    profileId: string;
    caption?: string | undefined;
}, {
    profileId: string;
    caption?: string | undefined;
}>;
export type UploadMediaRequest = z.infer<typeof UploadMediaRequestSchema>;
export declare const FamilyMemberSchema: z.ZodObject<{
    id: z.ZodString;
    familyId: z.ZodString;
    userId: z.ZodString;
    role: z.ZodEnum<["admin", "editor", "viewer"]>;
    invitedBy: z.ZodString;
    invitedAt: z.ZodDate;
    joinedAt: z.ZodOptional<z.ZodDate>;
    status: z.ZodEnum<["pending", "active", "inactive"]>;
}, "strip", z.ZodTypeAny, {
    id: string;
    userId: string;
    familyId: string;
    status: "pending" | "active" | "inactive";
    role: "admin" | "editor" | "viewer";
    invitedBy: string;
    invitedAt: Date;
    joinedAt?: Date | undefined;
}, {
    id: string;
    userId: string;
    familyId: string;
    status: "pending" | "active" | "inactive";
    role: "admin" | "editor" | "viewer";
    invitedBy: string;
    invitedAt: Date;
    joinedAt?: Date | undefined;
}>;
export type FamilyMember = z.infer<typeof FamilyMemberSchema>;
export declare const InviteFamilyMemberSchema: z.ZodObject<{
    email: z.ZodString;
    role: z.ZodDefault<z.ZodEnum<["editor", "viewer"]>>;
    message: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    email: string;
    role: "editor" | "viewer";
    message?: string | undefined;
}, {
    email: string;
    message?: string | undefined;
    role?: "editor" | "viewer" | undefined;
}>;
export type InviteFamilyMemberRequest = z.infer<typeof InviteFamilyMemberSchema>;
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
export interface ApiError {
    code: string;
    message: string;
    field?: string;
    details?: any;
}
export declare class AppError extends Error {
    statusCode: number;
    code: string;
    field?: string | undefined;
    details?: any | undefined;
    constructor(statusCode: number, code: string, message: string, field?: string | undefined, details?: any | undefined);
}
export type Partial<T> = {
    [P in keyof T]?: T[P];
};
export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;
export type WithTimestamps<T> = T & {
    createdAt: Date;
    updatedAt: Date;
};
export declare const PRIVACY_LEVELS: readonly ["public", "family", "private"];
export declare const FAMILY_ROLES: readonly ["admin", "editor", "viewer"];
export declare const MEDIA_TYPES: readonly ["image", "video", "document"];
export declare const MEMBER_STATUS: readonly ["pending", "active", "inactive"];
export declare const FILE_UPLOAD_LIMITS: {
    readonly IMAGE_MAX_SIZE: number;
    readonly VIDEO_MAX_SIZE: number;
    readonly DOCUMENT_MAX_SIZE: number;
    readonly ALLOWED_IMAGE_TYPES: readonly ["image/jpeg", "image/png", "image/webp"];
    readonly ALLOWED_VIDEO_TYPES: readonly ["video/mp4", "video/webm"];
    readonly ALLOWED_DOCUMENT_TYPES: readonly ["application/pdf", "text/plain"];
};
export declare const VIETNAMESE_MONTHS: readonly ["Tháng Giêng", "Tháng Hai", "Tháng Ba", "Tháng Tư", "Tháng Năm", "Tháng Sáu", "Tháng Bảy", "Tháng Tám", "Tháng Chín", "Tháng Mười", "Tháng Mười Một", "Tháng Chạp"];
//# sourceMappingURL=index.d.ts.map