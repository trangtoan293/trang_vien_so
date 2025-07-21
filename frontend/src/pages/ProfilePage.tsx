import React from 'react'
import { useAuthStore } from '@/store/authStore'

const ProfilePage: React.FC = () => {
  const { user } = useAuthStore()

  return (
    <div className="space-y-8">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Hồ sơ cá nhân</h1>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-gray-700">Họ</label>
            <p className="mt-1 text-sm text-gray-900">{user?.first_name}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Tên</label>
            <p className="mt-1 text-sm text-gray-900">{user?.last_name}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <p className="mt-1 text-sm text-gray-900">{user?.email}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Số điện thoại</label>
            <p className="mt-1 text-sm text-gray-900">{user?.phone_number || 'Chưa cập nhật'}</p>
          </div>
        </div>
        
        <div className="mt-6">
          <button
            type="button"
            className="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md"
          >
            Chỉnh sửa thông tin
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage