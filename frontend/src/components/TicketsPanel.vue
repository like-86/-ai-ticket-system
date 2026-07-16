<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['close'])

const tickets = ref([])
const loading = ref(false)
const selectedTicket = ref(null)
const detailLoading = ref(false)

async function fetchTickets() {
  loading.value = true
  try {
    const res = await fetch('/api/tickets')
    tickets.value = await res.json()
  } catch (err) {
    tickets.value = []
  } finally {
    loading.value = false
  }
}

async function viewDetail(ticket) {
  if (selectedTicket.value?.id === ticket.id) {
    selectedTicket.value = null
    return
  }
  detailLoading.value = true
  try {
    const res = await fetch(`/api/tickets/${ticket.id}`)
    selectedTicket.value = await res.json()
  } catch {
    selectedTicket.value = null
  } finally {
    detailLoading.value = false
  }
}

const STATUS_MAP = {
  pending: '待处理',
  processing: '处理中',
  resolved: '已解决',
  closed: '已关闭'
}
const PRIORITY_MAP = {
  low: '低',
  normal: '普通',
  high: '高',
  urgent: '紧急'
}

onMounted(fetchTickets)
</script>

<template>
  <div class="panel-overlay" @click.self="emit('close')">
    <div class="panel">
      <header class="panel-header">
        <h2>📋 工单列表</h2>
        <button class="close-btn" @click="emit('close')">✕</button>
      </header>

      <div v-if="loading" class="panel-loading">加载中...</div>

      <div v-else-if="tickets.length === 0" class="panel-empty">
        暂无工单
      </div>

      <div v-else class="panel-list">
        <div
          v-for="t in tickets"
          :key="t.id"
          class="ticket-item"
          :class="{ active: selectedTicket?.id === t.id }"
          @click="viewDetail(t)"
        >
          <div class="ticket-title">#{{ t.id }} {{ t.title }}</div>
          <div class="ticket-meta">
            <span :class="['status-badge', t.status]">{{ STATUS_MAP[t.status] || t.status }}</span>
            <span class="priority-badge">{{ PRIORITY_MAP[t.priority] || t.priority }}</span>
            <span class="ticket-date">{{ t.created_at?.slice(0, 10) }}</span>
          </div>

          <!-- 展开详情 -->
          <div v-if="selectedTicket?.id === t.id" class="ticket-detail">
            <div v-if="detailLoading">加载详情中...</div>
            <div v-else>
              <p>{{ selectedTicket.description }}</p>
              <div class="detail-row">
                <span>状态：{{ STATUS_MAP[selectedTicket.status] || selectedTicket.status }}</span>
                <span>优先级：{{ PRIORITY_MAP[selectedTicket.priority] || selectedTicket.priority }}</span>
              </div>
              <div class="detail-row">
                <span>创建时间：{{ selectedTicket.created_at }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.panel-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  z-index: 100;
  display: flex;
  justify-content: flex-end;
}
.panel {
  width: 420px;
  max-width: 90vw;
  height: 100%;
  background: #fff;
  display: flex;
  flex-direction: column;
  animation: slideIn 0.2s ease;
}
@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}
.panel-header h2 {
  font-size: 16px;
  color: #333;
}
.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
  padding: 4px 8px;
  border-radius: 4px;
}
.close-btn:hover {
  background: #f0f2f5;
  color: #333;
}

.panel-loading,
.panel-empty {
  padding: 40px 20px;
  text-align: center;
  color: #999;
  font-size: 14px;
}

.panel-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.ticket-item {
  padding: 14px 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.15s;
}
.ticket-item:hover {
  border-color: #1a73e8;
  background: #f8faff;
}
.ticket-item.active {
  border-color: #1a73e8;
  background: #f0f6ff;
}

.ticket-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ticket-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 12px;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}
.status-badge.pending { background: #fff3e0; color: #e65100; }
.status-badge.processing { background: #e3f2fd; color: #1565c0; }
.status-badge.resolved { background: #e8f5e9; color: #2e7d32; }
.status-badge.closed { background: #f5f5f5; color: #616161; }

.priority-badge {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
  background: #f0f2f5;
  color: #666;
}

.ticket-date {
  color: #999;
  margin-left: auto;
}

.ticket-detail {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}
.ticket-detail p {
  margin-bottom: 8px;
}
.detail-row {
  display: flex;
  gap: 16px;
  margin-top: 4px;
}
</style>
