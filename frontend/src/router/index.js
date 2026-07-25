import { createRouter, createWebHistory } from 'vue-router'

const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const ChatPage = () => import('../views/ChatPage.vue')

const routes = [
  {
    path: '/login',
    component: Login
  },
  {
    path: '/register',
    component: Register
  },
  {
    path: '/',
    component: ChatPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    // 登录/注册页
    if (to.path === '/login' || to.path === '/register') {
      if (token) next('/')
      else next()
    } else {
      // 无token直接踢登录
      if (!token) next('/login')
      else next()
    }
  })

export default router