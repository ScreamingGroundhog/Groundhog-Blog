import { defineStore } from "pinia";
import api from "../api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      const { data } = await api.post("/auth/login", { username, password });
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem("token", data.token);
    },
    async register(username, password, nickname) {
      const { data } = await api.post("/auth/register", {
        username,
        password,
        nickname,
      });
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem("token", data.token);
    },
    async fetchMe() {
      const { data } = await api.get("/auth/me");
      this.user = data;
    },
    logout() {
      this.token = "";
      this.user = null;
      localStorage.removeItem("token");
    },
  },
});
