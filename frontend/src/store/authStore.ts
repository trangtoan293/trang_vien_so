import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import toast from 'react-hot-toast'
import { api } from '@/services/api'
import { User, LoginRequest, RegisterRequest } from '@/types'

interface AuthState {
  // State
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  login: (credentials: LoginRequest) => Promise<void>
  register: (userData: RegisterRequest) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
  updateProfile: (userData: Partial<User>) => Promise<void>
  changePassword: (data: { current_password: string; new_password: string }) => Promise<void>
  clearError: () => void
  setLoading: (loading: boolean) => void
  initialize: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Actions
      login: async (credentials: LoginRequest) => {
        try {
          set({ isLoading: true, error: null })

          const response = await api.login(credentials)
          
          if (response.success) {
            // Store tokens
            api.setAuthTokens(response.tokens)
            
            // Update state
            set({
              user: response.user,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            })

            toast.success(`Chào mừng trở lại, ${response.user.first_name}!`)
          } else {
            throw new Error(response.message || 'Đăng nhập thất bại')
          }
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 
                             error.message || 
                             'Đăng nhập thất bại'
          
          set({
            error: errorMessage,
            isLoading: false,
            isAuthenticated: false,
            user: null,
          })

          toast.error(errorMessage)
          throw error
        }
      },

      register: async (userData: RegisterRequest) => {
        try {
          set({ isLoading: true, error: null })

          const response = await api.register(userData)
          
          if (response.success) {
            // Store tokens
            api.setAuthTokens(response.tokens)
            
            // Update state
            set({
              user: response.user,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            })

            toast.success(`Đăng ký thành công! Chào mừng ${response.user.first_name}!`)
          } else {
            throw new Error(response.message || 'Đăng ký thất bại')
          }
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 
                             error.message || 
                             'Đăng ký thất bại'
          
          set({
            error: errorMessage,
            isLoading: false,
            isAuthenticated: false,
            user: null,
          })

          toast.error(errorMessage)
          throw error
        }
      },

      logout: async () => {
        try {
          set({ isLoading: true })
          
          // Call logout API
          await api.logout()
        } catch (error) {
          console.error('Logout error:', error)
        } finally {
          // Always clear local state
          api.clearAuthTokens()
          
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          })

          toast.success('Đã đăng xuất thành công')
        }
      },

      refreshUser: async () => {
        try {
          if (!api.isAuthenticated()) {
            return
          }

          set({ isLoading: true, error: null })
          
          const user = await api.getCurrentUser()
          
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          })
        } catch (error: any) {
          console.error('Refresh user error:', error)
          
          // If token is invalid, logout
          if (error.response?.status === 401) {
            await get().logout()
          } else {
            set({
              error: error.message || 'Không thể tải thông tin người dùng',
              isLoading: false,
            })
          }
        }
      },

      updateProfile: async (userData: Partial<User>) => {
        try {
          set({ isLoading: true, error: null })

          const updatedUser = await api.updateProfile(userData)
          
          set({
            user: updatedUser,
            isLoading: false,
            error: null,
          })

          toast.success('Cập nhật thông tin thành công!')
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 
                             error.message || 
                             'Cập nhật thông tin thất bại'
          
          set({
            error: errorMessage,
            isLoading: false,
          })

          toast.error(errorMessage)
          throw error
        }
      },

      changePassword: async (data: { current_password: string; new_password: string }) => {
        try {
          set({ isLoading: true, error: null })

          await api.changePassword(data)
          
          set({
            isLoading: false,
            error: null,
          })

          toast.success('Đổi mật khẩu thành công!')
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 
                             error.message || 
                             'Đổi mật khẩu thất bại'
          
          set({
            error: errorMessage,
            isLoading: false,
          })

          toast.error(errorMessage)
          throw error
        }
      },

      clearError: () => {
        set({ error: null })
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading })
      },

      initialize: async () => {
        try {
          // Check if we have tokens in localStorage
          if (api.isAuthenticated()) {
            // First check if token is expired locally (faster than API call)
            if (api.isTokenExpired()) {
              console.log('Token expired, clearing authentication')
              api.clearAuthTokens()
              set({
                user: null,
                isAuthenticated: false,
                isLoading: false,
                error: null,
              })
              return
            }

            set({ isLoading: true })
            
            // Token is not expired, try to get user data
            try {
              const user = await api.getCurrentUser()
              
              set({
                user,
                isAuthenticated: true,
                isLoading: false,
                error: null,
              })
              return
            } catch (userError: any) {
              console.log('Getting current user failed:', userError.message)
              
              // If it's a 401 error, token is invalid despite not appearing expired
              if (userError.response?.status === 401) {
                console.log('Token invalid, clearing authentication')
                api.clearAuthTokens()
                set({
                  user: null,
                  isAuthenticated: false,
                  isLoading: false,
                  error: null,
                })
              } else {
                // Network error - use cached user data if available
                const currentState = get()
                if (currentState.user && currentState.isAuthenticated) {
                  console.log('Network error, using cached authentication')
                  set({
                    isLoading: false,
                    error: 'Using cached authentication (offline)',
                  })
                } else {
                  // No cached data, clear auth state
                  set({
                    user: null,
                    isAuthenticated: false,
                    isLoading: false,
                    error: null,
                  })
                }
              }
            }
          } else {
            // No tokens found - ensure clean state
            set({
              user: null,
              isAuthenticated: false,
              isLoading: false,
              error: null,
            })
          }
        } catch (error) {
          console.error('Initialize auth error:', error)
          
          // Fallback to clean state
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          })
        }
      },
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({
        // Only persist user data, not loading states or errors
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Export individual actions for convenience
export const {
  login,
  register,
  logout,
  refreshUser,
  updateProfile,
  changePassword,
  clearError,
  initialize,
} = useAuthStore.getState()

// Utility selectors
export const useUser = () => useAuthStore((state) => state.user)
export const useIsAuthenticated = () => useAuthStore((state) => state.isAuthenticated)
export const useAuthLoading = () => useAuthStore((state) => state.isLoading)
export const useAuthError = () => useAuthStore((state) => state.error)