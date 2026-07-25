import axios from 'axios'
import router from '../router'

const service = axios.create({
  baseURL: '/api',
  timeout: 10000
})

service.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  const isAuthApi = config.url.includes('/auth/login') || config.url.includes('/auth/register')
  if (token && !isAuthApi) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 直接返回 res.data，组件拿到的就是后端原始json
service.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
    return Promise.reject(err)
  }
)

export default service