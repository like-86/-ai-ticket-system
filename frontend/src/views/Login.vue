<template>
    <div class="login-wrap">
      <div class="login-card">
        <h2 class="login-title">🤖 AI 工单助手登录</h2>
        <div class="form-item">
          <label class="label">用户名</label>
          <input
            v-model="username"
            type="text"
            class="input"
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-item">
          <label class="label">密码</label>
          <input
            v-model="password"
            type="password"
            class="input"
            placeholder="请输入密码"
          />
        </div>
        <button class="login-btn" @click="handleLogin">登录</button>
        <div class="tip-text" @click="$router.push('/register')">
          没有账号？立即注册
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import request from '../utils/request'
  
  const router = useRouter()
  const username = ref('')
  const password = ref('')
  
  const handleLogin = async () => {
    // 这里必须先声明 un 和 pwd 变量
    const un = username.value.trim()
    const pwd = password.value.trim()
  
    if (!un || !pwd) {
      alert('用户名和密码不能为空')
      return
    }
  
    try {
      const res = await request.post('/auth/login', {
        username: un,
        password: pwd
      })
      console.log('登录返回：', res)
      if (res.token) {
        localStorage.setItem('token', res.token)
        router.push('/')
      } else {
        alert('登录失败，未获取到token')
      }
    } catch (err) {
      alert('请求异常：' + err.message)
    }
  }
  </script>
  
  <style scoped>
  .login-wrap {
    width: 100vw;
    height: 100vh;
    background-color: #f5f7fa;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .login-card {
    width: 380px;
    background: #ffffff;
    padding: 36px 32px;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(26, 115, 232, 0.08);
  }
  
  .login-title {
    text-align: center;
    color: #202124;
    font-size: 22px;
    margin: 0 0 30px;
    font-weight: 600;
  }
  
  .form-item {
    margin-bottom: 22px;
  }
  
  .label {
    display: block;
    font-size: 14px;
    color: #5f6368;
    margin-bottom: 8px;
  }
  
  .input {
    width: 100%;
    box-sizing: border-box;
    padding: 12px 16px;
    border: 1px solid #dadce0;
    border-radius: 10px;
    font-size: 15px;
    transition: border 0.2s ease;
  }
  
  .input:focus {
    outline: none;
    border-color: #1a73e8;
  }
  
  .login-btn {
    width: 100%;
    padding: 12px;
    background-color: #1a73e8;
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease;
  }
  
  .login-btn:hover {
    background-color: #1557b0;
  }
  
  .tip-text {
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
    color: #1a73e8;
    cursor: pointer;
  }
  
  .tip-text:hover {
    text-decoration: underline;
  }
  </style>