import React, { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

// Pages
import LandingPage from '@/pages/LandingPage'
import LoginPage from '@/pages/auth/LoginPage'
import RegisterPage from '@/pages/auth/RegisterPage'
import DashboardPage from '@/pages/DashboardPage'
import ProfilePage from '@/pages/ProfilePage'
import DeceasedProfilesPage from '@/pages/deceased/DeceasedProfilesPage'
import DeceasedProfileDetailPage from '@/pages/deceased/DeceasedProfileDetailPage'
import CreateDeceasedProfilePage from '@/pages/deceased/CreateDeceasedProfilePage'
import EditDeceasedProfilePage from '@/pages/deceased/EditDeceasedProfilePage'
import NotFoundPage from '@/pages/NotFoundPage'

// Layout
import Layout from '@/components/layout/Layout'
import AuthLayout from '@/components/layout/AuthLayout'

// Protected Route Component
interface ProtectedRouteProps {
  children: React.ReactNode
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuthStore()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

// Public Route Component (redirects if authenticated)
interface PublicRouteProps {
  children: React.ReactNode
}

const PublicRoute: React.FC<PublicRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuthStore()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

function App() {
  const { initialize, isLoading } = useAuthStore()

  useEffect(() => {
    // Initialize auth state on app start
    initialize()
  }, [initialize])

  // Show loading spinner during app initialization
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-sm text-gray-600">Đang tải ứng dụng...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="App">
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        
        {/* Auth Routes */}
        <Route path="/login" element={
          <PublicRoute>
            <AuthLayout>
              <LoginPage />
            </AuthLayout>
          </PublicRoute>
        } />
        
        <Route path="/register" element={
          <PublicRoute>
            <AuthLayout>
              <RegisterPage />
            </AuthLayout>
          </PublicRoute>
        } />

        {/* Protected Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Layout>
              <DashboardPage />
            </Layout>
          </ProtectedRoute>
        } />

        <Route path="/profile" element={
          <ProtectedRoute>
            <Layout>
              <ProfilePage />
            </Layout>
          </ProtectedRoute>
        } />

        {/* Deceased Profile Routes */}
        <Route path="/deceased" element={
          <ProtectedRoute>
            <Layout>
              <DeceasedProfilesPage />
            </Layout>
          </ProtectedRoute>
        } />

        <Route path="/deceased/create" element={
          <ProtectedRoute>
            <Layout>
              <CreateDeceasedProfilePage />
            </Layout>
          </ProtectedRoute>
        } />

        <Route path="/deceased/:id" element={
          <ProtectedRoute>
            <Layout>
              <DeceasedProfileDetailPage />
            </Layout>
          </ProtectedRoute>
        } />

        <Route path="/deceased/:id/edit" element={
          <ProtectedRoute>
            <Layout>
              <EditDeceasedProfilePage />
            </Layout>
          </ProtectedRoute>
        } />

        {/* Catch-all route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  )
}

export default App