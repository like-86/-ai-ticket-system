<template>
    <div class="panel-mask" @click.self="$emit('close')">
      <div class="panel-box">
        <div class="panel-header">
          <h3>📋 我的工单</h3>
          <button class="close-btn" @click="$emit('close')">×</button>
        </div>
  
        <!-- 加载中 -->
        <div class="loading" v-if="loading">加载中...</div>
  
        <!-- 空状态 -->
        <div class="empty" v-else-if="list.length === 0">
          <div class="empty-icon">📭</div>
          <p>暂无工单记录</p>
        </div>
  
        <!-- 工单列表 -->
        <div class="ticket-list" v-else>
          <div
            class="ticket-item"
            v-for="item in list"
            :key="item.id"
          >
            <div class="ticket-top">
              <span class="ticket-title">{{ item.title }}</span>
              <span :class="['status-tag', item.status]">{{ statusMap[item.status] }}</span>
            </div>
            <div class="ticket-desc">{{ item.description }}</div>
            <div class="ticket-bottom">
              <span class="priority">优先级：{{ priorityMap[item.priority] }}</span>
              <span class="ticket-time">{{ item.created_at }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, reactive } from 'vue'
  import request from '../utils/request'
  
  defineEmits(['close'])
  
  const loading = ref(false)
  const list = ref([])
  
  // 状态中英文映射
  const statusMap = reactive({
    pending: '待处理',
    processing: '处理中',
    done: '已完成'
  })
  
  // 优先级映射
  const priorityMap = reactive({
    low: '低',
    normal: '普通',
    high: '高',
    urgent: '紧急'
  })
  
  const fetchTickets = async () => {
    loading.value = true
    try {
      // 后端直接返回数组，直接赋值，不要再取 .data
      const res = await request.get('/tickets')
      console.log('工单返回：', res)
      list.value = res
    } catch (err) {
      console.error('获取工单失败：', err)
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    fetchTickets()
  })
  </script>
  
  <style scoped>
  .panel-mask {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
    backdrop-filter: blur(4px);
  }
  
  .panel-box {
    width: 560px;
    max-height: 70vh;
    background: #fff;
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  }
  
  .panel-header {
    padding: 18px 24px;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
  }
  
  .panel-header h3 {
    margin: 0;
    font-size: 17px;
    font-weight: 600;
  }
  
  .close-btn {
    width: 28px;
    height: 28px;
    border: none;
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .close-btn:hover {
    background: rgba(255, 255, 255, 0.3);
  }
  
  .loading, .empty {
    padding: 60px 20px;
    text-align: center;
    color: #999;
  }
  
  .empty-icon {
    font-size: 48px;
    margin-bottom: 12px;
  }
  
  .ticket-list {
    flex: 1;
    overflow-y: auto;
    padding: 16px 24px 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .ticket-item {
    padding: 14px 16px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background: #f9fafb;
    transition: all 0.2s;
  }
  
  .ticket-item:hover {
    border-color: #667eea;
    background: #fff;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.08);
  }
  
  .ticket-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  
  .ticket-title {
    font-weight: 600;
    color: #1f2937;
    font-size: 15px;
  }
  
  .status-tag {
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
  }
  
  .status-tag.pending {
    background: #fef3c7;
    color: #d97706;
  }
  
  .status-tag.processing {
    background: #dbeafe;
    color: #2563eb;
  }
  
  .status-tag.done {
    background: #d1fae5;
    color: #059669;
  }
  
  .ticket-desc {
    color: #6b7280;
    font-size: 13px;
    line-height: 1.5;
    margin-bottom: 10px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .ticket-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .priority {
    font-size: 12px;
    color: #6b7280;
  }
  
  .ticket-time {
    font-size: 12px;
    color: #9ca3af;
  }
  </style>