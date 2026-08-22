import { defineStore } from "pinia";
import api from "../services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem("access_token") || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async register(username, handle, password) {
      await api.post("/auth/register/", { username, handle, password });
    },

    async login(username, password) {
      const { data } = await api.post("/auth/login/", { username, password });
      this.accessToken = data.access;
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      await this.fetchMe();
    },

    async fetchMe() {
      const { data } = await api.get("/auth/me/");
      this.user = data;
    },

    logout() {
      this.user = null;
      this.accessToken = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
  },
});