<template>
    <div class="register-wrap">
      <div class="register-card">
        <h2 class="title">🤖 用户注册</h2>
  
        <div class="form-item">
          <label class="label">用户名</label>
          <input
            v-model="username"
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
  
        <div class="form-item">
          <label class="label">确认密码</label>
          <input
            v-model="repPwd"
            type="password"
            class="input"
            placeholder="再次输入密码"
          />
        </div>
  
        <button class="reg-btn" @click="handleRegister" :disabled="loading">
          {{ loading ? "注册中..." : "注册" }}
        </button>
  
        <div class="tip" @click="$router.push('/login')">
          已有账号？去登录
        </div>
      </div>
    </div>
  </template>
  
<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import request from '../utils/request'
  
  const router = useRouter()
  const username = ref('')
  const password = ref('')
  const repPwd = ref('')
  const loading = ref(false)
  
const handleRegister = async () => {
    
    const un = username.value.trim()
    const pwd = password.value.trim()
    const rp = repPwd.value.trim()
    if (!un || !pwd) return ElMessage.warning('账号密码不能为空')
    if (pwd !== rp) return ElMessage.warning('两次密码不一致')
  
    loading.value = true
    try {
      await request.post('/auth/register', { username: un, password: pwd })
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } catch (err) {
      ElMessage.error(err.response?.data?.msg || '注册失败')
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .register-wrap {
    width: 100vw;
    height: 100vh;
    background-color: #f5f7fa;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .register-card {
    width: 380px;
    background: #fff;
    padding: 36px 32px;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(26, 115, 232, 0.08);
  }
  
  .title {
    text-align: center;
    font-size: 22px;
    color: #202124;
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
  
  .reg-btn {
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
  
  .reg-btn:hover:not(:disabled) {
    background-color: #1557b0;
  }
  
  .reg-btn:disabled {
    background: #a0c4f0;
    cursor: not-allowed;
  }
  
  .tip {
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
    color: #1a73e8;
    cursor: pointer;
  }
  
  .tip:hover {
    text-decoration: underline;
  }
  </style>