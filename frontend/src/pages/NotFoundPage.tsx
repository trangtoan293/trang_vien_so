import React from 'react'
import { Link } from 'react-router-dom'

const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center">
      <div className="max-w-md mx-auto text-center">
        <div className="text-6xl mb-6">🏛️</div>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Trang không tồn tại
        </h1>
        <p className="text-gray-600 mb-8">
          Xin lỗi, chúng tôi không thể tìm thấy trang bạn đang tìm kiếm.
        </p>
        <Link
          to="/"
          className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          Quay về trang chủ
        </Link>
      </div>
    </div>
  )
}

export default NotFoundPage