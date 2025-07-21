import React from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { 
  PlusIcon, 
  UsersIcon, 
  CalendarDaysIcon,
  ChartBarIcon,
  HeartIcon 
} from '@heroicons/react/24/outline'

const DashboardPage: React.FC = () => {
  const { user } = useAuthStore()

  const quickActions = [
    {
      name: 'Thêm hồ sơ mới',
      description: 'Tạo hồ sơ tưởng niệm cho người thân',
      href: '/deceased/create',
      icon: PlusIcon,
      color: 'bg-primary-500 hover:bg-primary-600'
    },
    {
      name: 'Xem tất cả hồ sơ',
      description: 'Duyệt qua các hồ sơ đã tạo',
      href: '/deceased',
      icon: UsersIcon,
      color: 'bg-memorial-500 hover:bg-memorial-600'
    },
    {
      name: 'Lịch kỷ niệm',
      description: 'Xem các ngày kỷ niệm quan trọng',
      href: '/calendar',
      icon: CalendarDaysIcon,
      color: 'bg-vietnam-red hover:bg-red-600'
    }
  ]

  const stats = [
    { name: 'Hồ sơ đã tạo', value: '0', icon: HeartIcon },
    { name: 'Ảnh đã tải lên', value: '0', icon: ChartBarIcon },
    { name: 'Gia đình kết nối', value: '0', icon: UsersIcon },
  ]

  return (
    <div className="space-y-8">
      {/* Welcome section */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Chào mừng, {user?.first_name}! 👋
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Cùng nhau gìn giữ những kỷ niệm quý giá về người thân yêu
            </p>
          </div>
          <div className="text-6xl">🏛️</div>
        </div>
      </div>

      {/* Quick actions */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">Thao tác nhanh</h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              to={action.href}
              className="group relative bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow duration-200"
            >
              <div>
                <span className={`inline-flex p-3 rounded-lg ${action.color} text-white`}>
                  <action.icon className="h-6 w-6" aria-hidden="true" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium text-gray-900 group-hover:text-primary-600">
                  <span className="absolute inset-0" aria-hidden="true" />
                  {action.name}
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  {action.description}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">Thống kê</h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {stats.map((stat) => (
            <div key={stat.name} className="bg-white overflow-hidden rounded-lg shadow">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <stat.icon className="h-6 w-6 text-gray-400" aria-hidden="true" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        {stat.name}
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {stat.value}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent activity placeholder */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Hoạt động gần đây</h2>
        <div className="text-center py-12">
          <HeartIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Chưa có hoạt động nào</p>
          <p className="text-sm text-gray-400 mt-2">
            Bắt đầu bằng cách tạo hồ sơ tưởng niệm đầu tiên
          </p>
          <Link
            to="/deceased/create"
            className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Tạo hồ sơ mới
          </Link>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage