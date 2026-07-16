<script setup>
import { ref, nextTick } from 'vue'
import TicketsPanel from './TicketsPanel.vue'

const messages = ref([
  { role: 'bot', content: '你好！我是 AI 工单助手，有什么可以帮你的？' }
])
const inputText = ref('')
const sending = ref(false)
const messageListRef = ref(null)
const showTickets = ref(false)

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
      const res = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      })

      const reader = res.body.getReader()
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
            if (data.done) {
              // 流式结束
            } else {
              messages.value[loadingIdx].content += data.token
              scrollToBottom()
            }
          }
        }
      }
    } catch (err) {
      messages.value[loadingIdx] = {
        role: 'bot',
        content: `❌  请求失败：${err.message}`
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
  <div class="chat-container">
    <header class="chat-header">
      <h1>🤖 AI 工单助手</h1>
      <button class="tickets-btn" @click="showTickets = true">📋 工单</button>
    </header>

    <main class="chat-messages" ref="messageListRef">
      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="['message', msg.role]"
      >
        <div class="bubble">{{ msg.content }}</div>
      </div>
    </main>

    <footer class="chat-input-area">
      <input
        v-model="inputText"
        type="text"
        placeholder="输入你的问题..."
        :disabled="sending"
        @keydown="onKeydown"
      />
      <button :disabled="sending || !inputText.trim()" @click="sendMessage">
        {{ sending ? '发送中...' : '发送' }}
      </button>
    </footer>

    <TicketsPanel v-if="showTickets" @close="showTickets = false" />
  </div>
</template>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  max-width: 800px;
  margin: 0 auto;
  background: #fff;
  box-shadow: 0 0 20px rgba(0,0,0,0.05);
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-header h1 {
  font-size: 18px;
  color: #333;
}
.tickets-btn {
  padding: 6px 14px;
  background: #f0f2f5;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  color: #555;
  transition: all 0.15s;
}
.tickets-btn:hover {
  background: #1a73e8;
  color: #fff;
  border-color: #1a73e8;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
}
.message.user {
  justify-content: flex-end;
}
.message.bot {
  justify-content: flex-start;
}

.bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
  font-size: 14px;
  word-break: break-word;
}
.message.user .bubble {
  background: #1a73e8;
  color: #fff;
  border-bottom-right-radius: 4px;
}
.message.bot .bubble {
  background: #f0f2f5;
  color: #333;
  border-bottom-left-radius: 4px;
}

.chat-input-area {
  display: flex;
  gap: 8px;
  padding: 16px 24px;
  border-top: 1px solid #eee;
  background: #fff;
}
.chat-input-area input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}
.chat-input-area input:focus {
  border-color: #1a73e8;
}
.chat-input-area input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}
.chat-input-area button {
  padding: 10px 24px;
  background: #1a73e8;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}
.chat-input-area button:hover:not(:disabled) {
  background: #1557b0;
}
.chat-input-area button:disabled {
  background: #a0c4ff;
  cursor: not-allowed;
}
</style>
