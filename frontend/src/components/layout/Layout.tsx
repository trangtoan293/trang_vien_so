import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import {
  HomeIcon,
  UserIcon,
  UsersIcon,
  PlusIcon,
  Bars3Icon,
  XMarkIcon,
  PowerIcon
} from '@heroicons/react/24/outline'
import { useState } from 'react'
import { clsx } from 'clsx'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const navigation = [
    { name: 'Trang chính', href: '/dashboard', icon: HomeIcon, current: location.pathname === '/dashboard' },
    { name: 'Hồ sơ cá nhân', href: '/profile', icon: UserIcon, current: location.pathname === '/profile' },
    { name: 'Người thân', href: '/deceased', icon: UsersIcon, current: location.pathname.startsWith('/deceased') },
  ]

  const handleLogout = async () => {
    try {
      await logout()
      navigate('/login')
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      <div className={clsx(
        'fixed inset-0 z-50 lg:hidden',
        sidebarOpen ? 'block' : 'hidden'
      )}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white">
          <div className="flex h-16 items-center justify-between px-6 border-b border-gray-200">
            <div className="flex items-center">
              <span className="text-2xl">🏛️</span>
              <span className="ml-2 text-lg font-semibold text-gray-900">Trang Viên Số</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>
          <nav className="mt-6 px-3">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setSidebarOpen(false)}
                className={clsx(
                  item.current
                    ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-700'
                    : 'text-gray-700 hover:bg-gray-50',
                  'group flex items-center px-3 py-2 text-sm font-medium rounded-l-md'
                )}
              >
                <item.icon className={clsx(
                  item.current ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500',
                  'mr-3 h-5 w-5'
                )} />
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex grow flex-col overflow-y-auto border-r border-gray-200 bg-white">
          <div className="flex h-16 items-center px-6 border-b border-gray-200">
            <span className="text-2xl">🏛️</span>
            <span className="ml-2 text-lg font-semibold text-gray-900">Trang Viên Số</span>
          </div>
          <nav className="mt-6 flex-1 px-3 space-y-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={clsx(
                  item.current
                    ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-700'
                    : 'text-gray-700 hover:bg-gray-50',
                  'group flex items-center px-3 py-2 text-sm font-medium rounded-l-md'
                )}
              >
                <item.icon className={clsx(
                  item.current ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500',
                  'mr-3 h-5 w-5'
                )} />
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>

      {/* Main content area */}
      <div className="lg:pl-64">
        {/* Top header */}
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
          <button
            type="button"
            className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Bars3Icon className="h-6 w-6" />
          </button>

          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div className="flex flex-1 items-center">
              <h1 className="text-lg font-semibold text-gray-900">
                {navigation.find(item => item.current)?.name || 'Trang Viên Số'}
              </h1>
            </div>

            {/* Quick actions */}
            <div className="flex items-center gap-x-4 lg:gap-x-6">
              <Link
                to="/deceased/create"
                className="inline-flex items-center gap-x-2 rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500"
              >
                <PlusIcon className="h-4 w-4" />
                <span className="hidden sm:block">Thêm hồ sơ</span>
              </Link>

              {/* User menu */}
              <div className="relative">
                <div className="flex items-center gap-x-3">
                  <div className="hidden lg:flex lg:flex-col lg:items-end">
                    <p className="text-sm font-medium text-gray-900">
                      {user?.first_name} {user?.last_name}
                    </p>
                    <p className="text-xs text-gray-500">{user?.email}</p>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-x-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    <PowerIcon className="h-4 w-4" />
                    <span className="hidden sm:block">Đăng xuất</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="py-6">
          <div className="px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout