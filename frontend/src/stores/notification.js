import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    toasts: []
  }),
  actions: {
    addToast(message, type = 'success', duration = 4000) {
      const id = Date.now() + Math.random().toString(36).substring(2, 9)
      this.toasts.push({ id, message, type })
      setTimeout(() => {
        this.removeToast(id)
      }, duration)
    },
    removeToast(id) {
      this.toasts = this.toasts.filter(t => t.id !== id)
    },
    showSuccess(message, duration) {
      this.addToast(message, 'success', duration)
    },
    showError(message, duration) {
      this.addToast(message, 'error', duration)
    },
    showWarning(message, duration) {
      this.addToast(message, 'warning', duration)
    },
    showInfo(message, duration) {
      this.addToast(message, 'info', duration)
    }
  }
})
