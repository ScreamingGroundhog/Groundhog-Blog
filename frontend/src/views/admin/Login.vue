<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-md">
      <h1 class="text-2xl font-bold text-center text-white mb-8">管理员登录</h1>
      <form @submit.prevent="handleLogin" class="bg-gray-900 rounded-lg p-6 border border-gray-800 space-y-4">
        <div>
          <label class="block text-sm text-gray-400 mb-1">用户名</label>
          <input
            v-model="username"
            type="text"
            required
            class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-gray-100 focus:outline-none focus:border-blue-500 transition-colors"
          />
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-1">密码</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-gray-100 focus:outline-none focus:border-blue-500 transition-colors"
          />
        </div>
        <div v-if="error" class="text-red-400 text-sm">{{ error }}</div>
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white py-2 rounded transition-colors"
        >
          {{ loading ? "登录中..." : "登录" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const auth = useAuthStore();

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

async function handleLogin() {
  loading.value = true;
  error.value = "";
  try {
    await auth.login(username.value, password.value);
    router.push("/admin");
  } catch (e) {
    error.value = e.response?.data?.error || "登录失败";
  } finally {
    loading.value = false;
  }
}
</script>
