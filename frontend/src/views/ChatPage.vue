<script setup>
  import { ref, nextTick } from 'vue'
  import request from '../utils/request'
  import { useRouter } from 'vue-router' 
  import TicketsPanel from './TicketsPanel.vue'
  
  const router = useRouter()
  
  const sessionId = ref(localStorage.getItem('session_id') || crypto.randomUUID())
  localStorage.setItem('session_id', sessionId.value)
  
  const messages = ref([
    { role: 'bot', content: '你好！我是 AI 工单助手，有什么可以帮你的？' }
  ])
  const inputText = ref('')
  const sending = ref(false)
  const messageListRef = ref(null)
  const showTickets = ref(false)
  
  const logout = () => {
    localStorage.removeItem('token')
    router.push('/login')
  }
  
  async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || sending.value) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''

  const loadingIdx = messages.value.length
  messages.value.push({ role: 'bot', content: '' })
  scrollToBottom()

  sending.value = true
  try {
    // 改用原生 fetch 实现流式读取
    const token = localStorage.getItem('token')
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        message: text,
        session_id: sessionId.value
      })
    })

    // 401 未授权处理
    if (response.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
      throw new Error('登录已过期')
    }

    if (!response.ok) {
      throw new Error(`请求失败：${response.status}`)
    }

    // 这里拿到的才是真正的 ReadableStream
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const parts = buffer.split('\n')
      buffer = parts.pop() || ''

      for (const line of parts) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6))
          if (!data.done) {
            messages.value[loadingIdx].content += data.token
            scrollToBottom()
          }
        }
      }
    }
  } catch (err) {
    messages.value[loadingIdx] = {
      role: 'bot',
      content: `❌ 请求失败：${err.message}`
    }
  } finally {
    sending.value = false
    scrollToBottom()
  }
}
  function onKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }
  
  async function scrollToBottom() {
    await nextTick()
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  }
  </script>
  
  <template>
    <div class="page-bg">
      <div class="chat-container">
        <header class="chat-header">
          <div class="header-left">
            <div class="avatar">🤖</div>
            <div class="header-info">
              <h1>AI 工单助手</h1>
              <span class="status">在线</span>
            </div>
          </div>
          <div class="header-right">
            <button class="tickets-btn" @click="showTickets = true">
              <span>📋</span> 工单
            </button>
            <button class="logout-btn" @click="logout">
              <span>🚪</span> 退出
            </button>
          </div>
        </header>
  
        <main class="chat-messages" ref="messageListRef">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="['message', msg.role]"
          >
            <div class="avatar-sm" v-if="msg.role === 'bot'">🤖</div>
            <div class="bubble">{{ msg.content }}</div>
          </div>
        </main>
  
        <footer class="chat-input-area">
          <input
            v-model="inputText"
            type="text"
            placeholder="输入你的问题，回车发送..."
            :disabled="sending"
            @keydown="onKeydown"
          />
          <button 
            class="send-btn"
            :disabled="sending || !inputText.trim()" 
            @click="sendMessage"
          >
            {{ sending ? '发送中...' : '发送' }}
          </button>
        </footer>
  
        <TicketsPanel v-if="showTickets" @close="showTickets = false" />
      </div>
    </div>
  </template>
  
  <style scoped>
  .page-bg {
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    box-sizing: border-box;
  }
  
  .chat-container {
    height: 90vh;
    max-height: 800px;
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 850px;
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    overflow: hidden;
  }
  
  .chat-header {
    padding: 16px 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #fff;
  }
  
  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .avatar {
    width: 44px;
    height: 44px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
  }
  
  .header-info h1 {
    font-size: 17px;
    margin: 0;
    font-weight: 600;
  }
  
  .status {
    font-size: 12px;
    opacity: 0.85;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  
  .status::before {
    content: '';
    width: 6px;
    height: 6px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
  }
  
  .header-right {
    display: flex;
    gap: 10px;
  }
  
  .tickets-btn,
  .logout-btn {
    padding: 8px 14px;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 10px;
    font-size: 13px;
    cursor: pointer;
    color: #fff;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  
  .tickets-btn:hover,
  .logout-btn:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-1px);
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    background: #f8f9fc;
  }
  
  .chat-messages::-webkit-scrollbar {
    width: 6px;
  }
  
  .chat-messages::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;
  }
  
  .message {
    display: flex;
    align-items: flex-end;
    gap: 8px;
  }
  
  .message.user {
    justify-content: flex-end;
  }
  
  .message.bot {
    justify-content: flex-start;
  }
  
  .avatar-sm {
    width: 32px;
    height: 32px;
    background: #e0e7ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
  }
  
  .bubble {
    max-width: 65%;
    padding: 12px 16px;
    border-radius: 16px;
    line-height: 1.6;
    font-size: 14px;
    word-break: break-word;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }
  
  .message.user .bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    border-bottom-right-radius: 4px;
  }
  
  .message.bot .bubble {
    background: #ffffff;
    color: #374151;
    border-bottom-left-radius: 4px;
    border: 1px solid #e5e7eb;
  }
  
  .chat-input-area {
    display: flex;
    gap: 12px;
    padding: 16px 20px;
    border-top: 1px solid #e5e7eb;
    background: #fff;
  }
  
  .chat-input-area input {
    flex: 1;
    padding: 12px 18px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    font-size: 14px;
    outline: none;
    background: #f9fafb;
    transition: all 0.2s ease;
  }
  
  .chat-input-area input:focus {
    border-color: #667eea;
    background: #fff;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  .chat-input-area input:disabled {
    background: #f3f4f6;
    cursor: not-allowed;
  }
  
  .send-btn {
    padding: 12px 28px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .send-btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
  }
  
  .send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  </style>