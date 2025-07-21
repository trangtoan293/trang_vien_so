import React from 'react'
import { Link } from 'react-router-dom'
import { PlusIcon, HeartIcon } from '@heroicons/react/24/outline'

const DeceasedProfilesPage: React.FC = () => {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Hồ sơ người thân</h1>
        <Link
          to="/deceased/create"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          Thêm hồ sơ mới
        </Link>
      </div>

      {/* Empty state */}
      <div className="bg-white rounded-lg shadow p-12">
        <div className="text-center">
          <HeartIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Chưa có hồ sơ nào
          </h3>
          <p className="text-gray-500 mb-6">
            Bắt đầu tạo hồ sơ tưởng niệm cho người thân yêu của bạn
          </p>
          <Link
            to="/deceased/create"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Tạo hồ sơ đầu tiên
          </Link>
        </div>
      </div>
    </div>
  )
}

export default DeceasedProfilesPage