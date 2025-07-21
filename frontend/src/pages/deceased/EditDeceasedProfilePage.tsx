import React from 'react'
import { useParams } from 'react-router-dom'

const EditDeceasedProfilePage: React.FC = () => {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="space-y-8">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Chỉnh sửa hồ sơ
        </h1>
        <div className="text-center py-12">
          <p className="text-gray-500">
            Tính năng đang phát triển... (ID: {id})
          </p>
        </div>
      </div>
    </div>
  )
}

export default EditDeceasedProfilePage