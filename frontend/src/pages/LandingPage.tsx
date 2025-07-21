import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRightIcon, HeartIcon, ShieldCheckIcon, GlobeAltIcon } from '@heroicons/react/24/outline'

const LandingPage: React.FC = () => {
  const features = [
    {
      name: 'Bảo tồn ký ức quý giá',
      description: 'Lưu trữ thông tin, hình ảnh và câu chuyện về người thân một cách an toàn và trang trọng.',
      icon: HeartIcon,
    },
    {
      name: 'Bảo mật tuyệt đối',
      description: 'Dữ liệu được mã hóa và bảo vệ bằng các biện pháp bảo mật tiên tiến nhất.',
      icon: ShieldCheckIcon,
    },
    {
      name: 'Văn hóa Việt Nam',
      description: 'Hỗ trợ âm lịch, tên thế hệ và các truyền thống văn hóa Việt Nam một cách chuyên sâu.',
      icon: GlobeAltIcon,
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl">🏛️</span>
              <span className="ml-2 text-xl font-bold text-gray-900">Trang Viên Số</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Đăng nhập
              </Link>
              <Link
                to="/register"
                className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Đăng ký
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero section */}
      <div className="relative bg-gradient-to-br from-primary-900 via-primary-800 to-memorial-900">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:py-32 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="text-8xl mb-8 text-white">🏛️</div>
            <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl">
              Trang Viên Số
            </h1>
            <p className="mt-6 text-xl leading-8 text-primary-100 max-w-3xl mx-auto">
              Nơi lưu trữ và tôn vinh kỷ niệm về những người thân yêu đã khuất. 
              Gìn giữ di sản gia đình với sự trang trọng và ý nghĩa sâu sắc.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                to="/register"
                className="rounded-md bg-white px-6 py-3 text-base font-semibold text-primary-900 shadow-sm hover:bg-gray-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                Bắt đầu ngay
              </Link>
              <Link
                to="/login"
                className="text-base font-semibold leading-6 text-white hover:text-primary-100"
              >
                Đã có tài khoản <ArrowRightIcon className="inline h-5 w-5 ml-1" />
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features section */}
      <div className="py-24 sm:py-32 bg-white">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-primary-600">
              Tính năng nổi bật
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Lưu trữ kỷ niệm một cách trang trọng
            </p>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Trang Viên Số được thiết kế đặc biệt để phù hợp với văn hóa và truyền thống Việt Nam, 
              giúp bạn tạo nên một không gian tưởng niệm đầy ý nghĩa.
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
              {features.map((feature) => (
                <div key={feature.name} className="flex flex-col">
                  <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                    <feature.icon className="h-5 w-5 flex-none text-primary-600" aria-hidden="true" />
                    {feature.name}
                  </dt>
                  <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                    <p className="flex-auto">{feature.description}</p>
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>

      {/* CTA section */}
      <div className="bg-primary-50">
        <div className="px-6 py-24 sm:px-6 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Bắt đầu hành trình tưởng niệm
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-600">
              Tạo tài khoản miễn phí và bắt đầu xây dựng không gian tưởng niệm 
              đầy ý nghĩa cho người thân yêu của bạn.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                to="/register"
                className="rounded-md bg-primary-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
              >
                Đăng ký miễn phí
              </Link>
              <Link
                to="/login"
                className="text-base font-semibold leading-6 text-gray-900 hover:text-primary-600"
              >
                Đăng nhập <ArrowRightIcon className="inline h-5 w-5 ml-1" />
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900">
        <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
          <div className="flex justify-center items-center">
            <div className="flex items-center">
              <span className="text-2xl">🏛️</span>
              <span className="ml-2 text-xl font-bold text-white">Trang Viên Số</span>
            </div>
          </div>
          <p className="mt-4 text-center text-sm leading-6 text-gray-400">
            &copy; 2024 Trang Viên Số. Lưu trữ kỷ niệm với tình yêu thương.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage