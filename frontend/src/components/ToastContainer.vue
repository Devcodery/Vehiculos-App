<template>
  <div class="toast-container">
    <TransitionGroup name="toast-slide">
      <div 
        v-for="toast in notificationStore.toasts" 
        :key="toast.id" 
        class="toast-item cell-shaded"
        :class="`toast-${toast.type}`"
      >
        <div class="toast-icon">
          <i v-if="toast.type === 'success'" class="fa-solid fa-circle-check"></i>
          <i v-else-if="toast.type === 'error'" class="fa-solid fa-triangle-exclamation"></i>
          <i v-else-if="toast.type === 'warning'" class="fa-solid fa-circle-exclamation"></i>
          <i v-else class="fa-solid fa-circle-info"></i>
        </div>
        
        <div class="toast-content">
          <span class="toast-title">{{ getToastTitle(toast.type) }}</span>
          <p class="toast-message">{{ toast.message }}</p>
        </div>

        <button @click="notificationStore.removeToast(toast.id)" class="toast-close-btn">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useNotificationStore } from '@/stores/notification'

const notificationStore = useNotificationStore()

const getToastTitle = (type) => {
  switch (type) {
    case 'success': return 'ÉXITO'
    case 'error': return 'ERROR'
    case 'warning': return 'ATENCIÓN'
    default: return 'INFO'
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 380px;
  width: 90%;
  pointer-events: none;
}

.toast-item {
  background: #111;
  border-width: 3px;
  border-style: solid;
  padding: 15px 20px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  position: relative;
  pointer-events: auto;
  box-shadow: 6px 6px 0 #000;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Toast types colors */
.toast-success {
  border-color: #00ff66 !important;
  box-shadow: 6px 6px 0 #000, 0 0 15px rgba(0, 255, 102, 0.2);
}
.toast-success .toast-icon {
  color: #00ff66;
}
.toast-success .toast-title {
  color: #00ff66;
}

.toast-error {
  border-color: #ff3366 !important;
  box-shadow: 6px 6px 0 #000, 0 0 15px rgba(255, 51, 102, 0.2);
}
.toast-error .toast-icon {
  color: #ff3366;
}
.toast-error .toast-title {
  color: #ff3366;
}

.toast-warning {
  border-color: #ffcc00 !important;
  box-shadow: 6px 6px 0 #000, 0 0 15px rgba(255, 204, 0, 0.2);
}
.toast-warning .toast-icon {
  color: #ffcc00;
}
.toast-warning .toast-title {
  color: #ffcc00;
}

.toast-info {
  border-color: #00e5ff !important;
  box-shadow: 6px 6px 0 #000, 0 0 15px rgba(0, 229, 255, 0.2);
}
.toast-info .toast-icon {
  color: #00e5ff;
}
.toast-info .toast-title {
  color: #00e5ff;
}

.toast-icon {
  font-size: 1.5rem;
  margin-top: 2px;
}

.toast-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toast-title {
  font-family: 'Bangers', cursive;
  font-size: 1.3rem;
  letter-spacing: 1px;
}

.toast-message {
  font-family: 'Roboto', sans-serif;
  color: #ddd;
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.4;
}

.toast-close-btn {
  background: transparent;
  border: none;
  color: #666;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  transition: color 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 3px;
}

.toast-close-btn:hover {
  color: #fff;
}

/* Animations */
.toast-slide-enter-from {
  opacity: 0;
  transform: translateX(100px) scale(0.9);
}
.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(100px) scale(0.9);
}
.toast-slide-leave-active {
  position: absolute;
}
</style>
