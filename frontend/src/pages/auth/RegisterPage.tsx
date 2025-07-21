import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

const RegisterPage: React.FC = () => {
  const navigate = useNavigate()
  const { register, isLoading, error } = useAuthStore()
  
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
    confirm_password: '',
    agree_terms: false
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({})

  const validateForm = () => {
    const errors: Record<string, string> = {}

    if (!formData.first_name.trim()) {
      errors.first_name = 'Họ là bắt buộc'
    }

    if (!formData.last_name.trim()) {
      errors.last_name = 'Tên là bắt buộc'
    }

    if (!formData.email) {
      errors.email = 'Email là bắt buộc'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email không hợp lệ'
    }

    if (formData.phone_number && !/^(\+84|84|0)[3-9]\d{8}$/.test(formData.phone_number)) {
      errors.phone_number = 'Số điện thoại không hợp lệ (VD: 0901234567)'
    }

    if (!formData.password) {
      errors.password = 'Mật khẩu là bắt buộc'
    } else if (formData.password.length < 8) {
      errors.password = 'Mật khẩu phải có ít nhất 8 ký tự'
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      errors.password = 'Mật khẩu phải có ít nhất 1 chữ hoa, 1 chữ thường và 1 số'
    }

    if (!formData.confirm_password) {
      errors.confirm_password = 'Xác nhận mật khẩu là bắt buộc'
    } else if (formData.password !== formData.confirm_password) {
      errors.confirm_password = 'Mật khẩu xác nhận không khớp'
    }

    if (!formData.agree_terms) {
      errors.agree_terms = 'Bạn phải đồng ý với điều khoản sử dụng'
    }

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    try {
      // Prepare data for API
      const registerData = {
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        email: formData.email.toLowerCase().trim(),
        password: formData.password,
        phone_number: formData.phone_number || undefined,
        language: 'vi',
        timezone: 'Asia/Ho_Chi_Minh'
      }

      await register(registerData)
      navigate('/dashboard')
    } catch (error) {
      // Error is handled by the auth store
      console.error('Registration failed:', error)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
    
    // Clear validation error when user starts typing
    if (validationErrors[name]) {
      setValidationErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  return (
    <div>
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900">
          Đăng ký tài khoản
        </h2>
        <p className="mt-2 text-sm text-gray-600">
          Tạo tài khoản để bắt đầu lưu trữ kỷ niệm người thân
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        {/* Name fields */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
              Họ <span className="text-red-500">*</span>
            </label>
            <div className="mt-1">
              <input
                id="first_name"
                name="first_name"
                type="text"
                autoComplete="given-name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="block w-full rounded-md border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
                placeholder="Nguyễn"
              />
              {validationErrors.first_name && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.first_name}</p>
              )}
            </div>
          </div>

          <div>
            <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
              Tên <span className="text-red-500">*</span>
            </label>
            <div className="mt-1">
              <input
                id="last_name"
                name="last_name"
                type="text"
                autoComplete="family-name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="block w-full rounded-md border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
                placeholder="Văn A"
              />
              {validationErrors.last_name && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.last_name}</p>
              )}
            </div>
          </div>
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email <span className="text-red-500">*</span>
          </label>
          <div className="mt-1">
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              value={formData.email}
              onChange={handleInputChange}
              className="block w-full rounded-md border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
              placeholder="your@email.com"
            />
            {validationErrors.email && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700">
            Số điện thoại
          </label>
          <div className="mt-1">
            <input
              id="phone_number"
              name="phone_number"
              type="tel"
              autoComplete="tel"
              value={formData.phone_number}
              onChange={handleInputChange}
              className="block w-full rounded-md border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
              placeholder="0901234567"
            />
            {validationErrors.phone_number && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.phone_number}</p>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Mật khẩu <span className="text-red-500">*</span>
          </label>
          <div className="mt-1 relative">
            <input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={formData.password}
              onChange={handleInputChange}
              className="block w-full rounded-md border-gray-300 px-3 py-2 pr-10 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
              placeholder="••••••••"
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <EyeSlashIcon className="h-5 w-5 text-gray-400" />
              ) : (
                <EyeIcon className="h-5 w-5 text-gray-400" />
              )}
            </button>
          </div>
          {validationErrors.password && (
            <p className="mt-1 text-sm text-red-600">{validationErrors.password}</p>
          )}
          <p className="mt-1 text-sm text-gray-500">
            Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường và số
          </p>
        </div>

        <div>
          <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700">
            Xác nhận mật khẩu <span className="text-red-500">*</span>
          </label>
          <div className="mt-1 relative">
            <input
              id="confirm_password"
              name="confirm_password"
              type={showConfirmPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={formData.confirm_password}
              onChange={handleInputChange}
              className="block w-full rounded-md border-gray-300 px-3 py-2 pr-10 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
              placeholder="••••••••"
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? (
                <EyeSlashIcon className="h-5 w-5 text-gray-400" />
              ) : (
                <EyeIcon className="h-5 w-5 text-gray-400" />
              )}
            </button>
          </div>
          {validationErrors.confirm_password && (
            <p className="mt-1 text-sm text-red-600">{validationErrors.confirm_password}</p>
          )}
        </div>

        <div className="flex items-start">
          <div className="flex items-center h-5">
            <input
              id="agree_terms"
              name="agree_terms"
              type="checkbox"
              checked={formData.agree_terms}
              onChange={handleInputChange}
              className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
            />
          </div>
          <div className="ml-3 text-sm">
            <label htmlFor="agree_terms" className="text-gray-700">
              Tôi đồng ý với{' '}
              <Link to="/terms" className="text-primary-600 hover:text-primary-500">
                điều khoản sử dụng
              </Link>{' '}
              và{' '}
              <Link to="/privacy" className="text-primary-600 hover:text-primary-500">
                chính sách bảo mật
              </Link>
              <span className="text-red-500"> *</span>
            </label>
            {validationErrors.agree_terms && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.agree_terms}</p>
            )}
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="flex items-center">
                <LoadingSpinner size="sm" color="white" className="mr-2" />
                Đang tạo tài khoản...
              </div>
            ) : (
              'Tạo tài khoản'
            )}
          </button>
        </div>

        <div className="text-center">
          <p className="text-sm text-gray-600">
            Đã có tài khoản?{' '}
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Đăng nhập ngay
            </Link>
          </p>
        </div>
      </form>
    </div>
  )
}

export default RegisterPage