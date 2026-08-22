import { defineStore } from "pinia";
import api from "../services/api";

export const useNotificationsStore = defineStore("notifications", {
  state: () => ({
    unreadCount: 0,
  }),
  actions: {
    async fetchUnreadCount() {
      try {
        const { data } = await api.get("/notifications/unread-count/");
        this.unreadCount = data.unread_count;
      } catch (e) {
        // silencioso - mantem o valor anterior se a chamada falhar
      }
    },
    async markAllRead() {
      await api.post("/notifications/mark-read/");
      this.unreadCount = 0;
    },
  },
});