import React from 'react'

interface AuthLayoutProps {
  children: React.ReactNode
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:flex-1 lg:flex-col lg:justify-center lg:px-20 bg-gradient-to-br from-primary-900 via-primary-800 to-memorial-900">
        <div className="text-center">
          <div className="text-6xl mb-6 text-white">🏛️</div>
          <h1 className="text-4xl font-bold text-white mb-4">
            Trang Viên Số
          </h1>
          <p className="text-xl text-primary-100 mb-8">
            Lưu trữ kỷ niệm người thân một cách trang trọng và ý nghĩa
          </p>
          <div className="text-primary-200 space-y-3">
            <p className="flex items-center justify-center">
              <span className="w-2 h-2 bg-vietnam-yellow rounded-full mr-3"></span>
              Bảo tồn ký ức quý giá
            </p>
            <p className="flex items-center justify-center">
              <span className="w-2 h-2 bg-vietnam-yellow rounded-full mr-3"></span>
              Kết nối gia đình yêu thương
            </p>
            <p className="flex items-center justify-center">
              <span className="w-2 h-2 bg-vietnam-yellow rounded-full mr-3"></span>
              Tôn vinh di sản văn hóa
            </p>
          </div>
        </div>
      </div>

      {/* Right side - Auth form */}
      <div className="flex-1 flex flex-col justify-center px-6 py-12 lg:px-20 lg:flex-none lg:w-1/2">
        <div className="mx-auto w-full max-w-md">
          {/* Mobile logo */}
          <div className="text-center mb-8 lg:hidden">
            <div className="text-4xl mb-3">🏛️</div>
            <h1 className="text-2xl font-bold text-gray-900">Trang Viên Số</h1>
            <p className="text-sm text-gray-600 mt-2">
              Lưu trữ kỷ niệm người thân
            </p>
          </div>

          {children}
        </div>
      </div>
    </div>
  )
}

export default AuthLayout