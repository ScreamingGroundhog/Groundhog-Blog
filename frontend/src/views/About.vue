<template>
  <div class="max-w-2xl mx-auto px-4 py-16">
    <div class="text-center mb-10">
      <div class="w-24 h-24 rounded-full bg-gray-800 mx-auto mb-4 flex items-center justify-center overflow-hidden">
        <img
          v-if="about.avatar"
          :src="about.avatar"
          :alt="about.nickname"
          class="w-full h-full object-cover"
        />
        <span v-else class="text-3xl text-gray-400 font-bold">{{ about.nickname?.charAt(0) || "?" }}</span>
      </div>
      <h1 class="text-2xl font-bold text-white mb-2">{{ about.nickname }}</h1>
      <p class="text-gray-400">{{ about.description || "这个人很懒，什么都没写..." }}</p>
    </div>

    <div class="bg-gray-900 rounded-lg p-6 border border-gray-800 space-y-4">
      <h3 class="text-lg font-semibold text-white mb-3">关于我</h3>
      <p class="text-gray-400 leading-relaxed">
        {{ about.description || "这是一个基于 Vue 3 + Flask + MySQL 构建的个人技术博客。专注于技术沉淀与知识分享，追求极致的阅读体验。" }}
      </p>
      <div class="flex gap-3 pt-2">
        <a
          v-if="about.github"
          :href="about.github"
          target="_blank"
          rel="noopener noreferrer"
          class="text-gray-400 hover:text-white transition-colors text-sm"
        >
          GitHub
        </a>
      </div>
    </div>

    <div class="bg-gray-900 rounded-lg p-6 border border-gray-800 mt-6">
      <h3 class="text-lg font-semibold text-white mb-3">技术栈</h3>
      <div class="grid grid-cols-2 gap-3 text-sm text-gray-400">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 bg-green-500 rounded-full"></span>
          Vue 3 + Vite
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 bg-blue-500 rounded-full"></span>
          Flask + SQLAlchemy
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 bg-yellow-500 rounded-full"></span>
          Tailwind CSS
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 bg-purple-500 rounded-full"></span>
          MySQL 8.x
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 bg-pink-500 rounded-full"></span>
          markdown-it
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 bg-orange-500 rounded-full"></span>
          JWT 认证
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const about = ref({
  nickname: "Admin",
  description: "",
  github: "https://github.com",
});

onMounted(async () => {
  try {
    const { data } = await api.get("/public/about");
    about.value = data;
  } catch {}
});
</script>
