import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import toast from 'react-hot-toast'
import { 
  LoginRequest, 
  LoginResponse, 
  RegisterRequest, 
  AuthTokens, 
  User,
  DeceasedProfile,
  DeceasedProfileCreate,
  DeceasedProfileUpdate,
  DeceasedProfileList
} from '@/types'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('access_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor - handle auth errors and token refresh
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response
      },
      async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            const refreshToken = localStorage.getItem('refresh_token')
            if (refreshToken) {
              const response = await this.client.post('/api/auth/refresh', {
                refresh_token: refreshToken,
              })

              const { access_token, refresh_token: newRefreshToken } = response.data.tokens
              
              localStorage.setItem('access_token', access_token)
              localStorage.setItem('refresh_token', newRefreshToken)

              // Retry original request with new token
              originalRequest.headers.Authorization = `Bearer ${access_token}`
              return this.client(originalRequest)
            }
          } catch (refreshError) {
            // Refresh failed, redirect to login
            this.handleAuthError()
            return Promise.reject(refreshError)
          }
        }

        // Handle other error responses
        if (error.response?.data?.detail) {
          toast.error(error.response.data.detail)
        } else if (error.message) {
          toast.error(error.message)
        }

        return Promise.reject(error)
      }
    )
  }

  private handleAuthError() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }

  // Generic request method
  private async request<T>(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    url: string,
    data?: any,
    config?: any
  ): Promise<T> {
    try {
      const response = await this.client.request({
        method,
        url,
        data,
        ...config,
      })
      return response.data
    } catch (error: any) {
      throw error.response?.data || error
    }
  }

  // Authentication methods
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    return this.request<LoginResponse>('POST', '/api/auth/login', credentials)
  }

  async register(userData: RegisterRequest): Promise<LoginResponse> {
    return this.request<LoginResponse>('POST', '/api/auth/register', userData)
  }

  async logout(): Promise<void> {
    try {
      await this.request('POST', '/api/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      this.handleAuthError() // Clear local storage regardless
    }
  }

  async refreshToken(): Promise<AuthTokens> {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    return this.request<AuthTokens>('POST', '/api/auth/refresh', {
      refresh_token: refreshToken,
    })
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('GET', '/api/auth/me')
  }

  async verifyToken(): Promise<{ valid: boolean }> {
    return this.request<{ valid: boolean }>('GET', '/api/auth/verify-token')
  }

  // User methods
  async updateProfile(userData: Partial<User>): Promise<User> {
    return this.request<User>('PUT', '/api/users/me', userData)
  }

  async changePassword(data: { 
    current_password: string
    new_password: string 
  }): Promise<void> {
    return this.request<void>('POST', '/api/users/change-password', data)
  }

  async deleteAccount(): Promise<void> {
    return this.request<void>('DELETE', '/api/users/me')
  }

  // Deceased Profile methods
  async createDeceasedProfile(profileData: DeceasedProfileCreate): Promise<DeceasedProfile> {
    return this.request<DeceasedProfile>('POST', '/api/deceased/', profileData)
  }

  async getDeceasedProfiles(params?: {
    skip?: number
    limit?: number
    family_id?: string
    search?: string
  }): Promise<DeceasedProfileList> {
    const searchParams = new URLSearchParams()
    
    if (params?.skip !== undefined) searchParams.append('skip', params.skip.toString())
    if (params?.limit !== undefined) searchParams.append('limit', params.limit.toString())
    if (params?.family_id) searchParams.append('family_id', params.family_id)
    if (params?.search) searchParams.append('search', params.search)

    const query = searchParams.toString()
    const url = query ? `/api/deceased/?${query}` : '/api/deceased/'
    
    return this.request<DeceasedProfileList>('GET', url)
  }

  async getDeceasedProfile(profileId: string): Promise<DeceasedProfile> {
    return this.request<DeceasedProfile>('GET', `/api/deceased/${profileId}`)
  }

  async updateDeceasedProfile(
    profileId: string, 
    profileData: DeceasedProfileUpdate
  ): Promise<DeceasedProfile> {
    return this.request<DeceasedProfile>('PUT', `/api/deceased/${profileId}`, profileData)
  }

  async deleteDeceasedProfile(profileId: string): Promise<void> {
    return this.request<void>('DELETE', `/api/deceased/${profileId}`)
  }

  // Media upload methods
  async uploadFile(file: File, profileId?: string): Promise<{ url: string; file_id: string }> {
    const formData = new FormData()
    formData.append('file', file)
    if (profileId) {
      formData.append('profile_id', profileId)
    }

    return this.request<{ url: string; file_id: string }>('POST', '/api/media/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.request<{ status: string; timestamp: string }>('GET', '/health')
  }

  // Utility methods
  getAuthToken(): string | null {
    return localStorage.getItem('access_token')
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  }

  isTokenExpired(): boolean {
    const token = localStorage.getItem('access_token')
    if (!token) return true
    
    try {
      // Decode JWT token (without verifying signature - just checking expiration)
      const base64Url = token.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      )
      const decoded = JSON.parse(jsonPayload)
      const currentTime = Date.now() / 1000
      
      return decoded.exp < currentTime
    } catch (error) {
      console.error('Error decoding token:', error)
      return true // Assume expired if we can't decode
    }
  }

  setAuthTokens(tokens: AuthTokens): void {
    localStorage.setItem('access_token', tokens.access_token)
    localStorage.setItem('refresh_token', tokens.refresh_token)
  }

  clearAuthTokens(): void {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }
}

// Create and export singleton instance
export const apiClient = new ApiClient()

// Export API methods for direct use
export const api = {
  // Authentication
  login: (credentials: LoginRequest) => apiClient.login(credentials),
  register: (userData: RegisterRequest) => apiClient.register(userData),
  logout: () => apiClient.logout(),
  getCurrentUser: () => apiClient.getCurrentUser(),
  verifyToken: () => apiClient.verifyToken(),
  
  // User management
  updateProfile: (userData: Partial<User>) => apiClient.updateProfile(userData),
  changePassword: (data: { current_password: string; new_password: string }) => 
    apiClient.changePassword(data),
  deleteAccount: () => apiClient.deleteAccount(),
  
  // Deceased profiles
  createDeceasedProfile: (data: DeceasedProfileCreate) => apiClient.createDeceasedProfile(data),
  getDeceasedProfiles: (params?: any) => apiClient.getDeceasedProfiles(params),
  getDeceasedProfile: (id: string) => apiClient.getDeceasedProfile(id),
  updateDeceasedProfile: (id: string, data: DeceasedProfileUpdate) => 
    apiClient.updateDeceasedProfile(id, data),
  deleteDeceasedProfile: (id: string) => apiClient.deleteDeceasedProfile(id),
  
  // Media
  uploadFile: (file: File, profileId?: string) => apiClient.uploadFile(file, profileId),
  
  // Utilities
  healthCheck: () => apiClient.healthCheck(),
  isAuthenticated: () => apiClient.isAuthenticated(),
  isTokenExpired: () => apiClient.isTokenExpired(),
  getAuthToken: () => apiClient.getAuthToken(),
  setAuthTokens: (tokens: AuthTokens) => apiClient.setAuthTokens(tokens),
  clearAuthTokens: () => apiClient.clearAuthTokens(),
}

export default api