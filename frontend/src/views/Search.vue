<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="mb-6">
      <input
        v-model="keyword"
        @keyup.enter="search"
        type="text"
        placeholder="搜索文章标题或内容..."
        class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
      />
      <button
        @click="search"
        class="mt-3 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
      >
        搜索
      </button>
    </div>

    <div v-if="loading" class="text-center text-gray-400 py-10">搜索中...</div>

    <template v-else>
      <p v-if="searched" class="text-gray-400 text-sm mb-4">
        找到 {{ total }} 篇相关文章
      </p>

      <div v-if="results.length === 0 && searched" class="text-center text-gray-500 py-10">
        未找到相关文章
      </div>

      <div class="space-y-4">
        <div
          v-for="article in results"
          :key="article.id"
          class="bg-gray-900 rounded-lg p-5 border border-gray-800 hover:border-gray-700 transition-colors"
        >
          <router-link
            :to="`/article/${article.id}`"
            class="text-lg font-bold text-white hover:text-blue-400 transition-colors"
          >
            {{ article.title }}
          </router-link>
          <p class="text-gray-400 text-sm mt-2 line-clamp-2">{{ article.summary }}</p>
          <div class="flex items-center gap-3 text-xs text-gray-500 mt-3">
            <span>{{ formatDate(article.created_at) }}</span>
            <span v-if="article.category">{{ article.category.name }}</span>
          </div>
        </div>
      </div>

      <Pagination
        v-if="totalPages > 1"
        :current-page="currentPage"
        :total-pages="totalPages"
        @change="(p) => search(p)"
      />
    </template>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../api";
import Pagination from "../components/Pagination.vue";

const keyword = ref("");
const results = ref([]);
const total = ref(0);
const currentPage = ref(1);
const totalPages = ref(1);
const loading = ref(false);
const searched = ref(false);

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("zh-CN");
}

async function search(page = 1) {
  if (!keyword.value.trim()) return;
  loading.value = true;
  searched.value = true;
  try {
    const { data } = await api.get("/public/articles", {
      params: { keyword: keyword.value.trim(), page, per_page: 10 },
    });
    results.value = data.items;
    total.value = data.total;
    currentPage.value = data.page;
    totalPages.value = data.pages;
  } catch (e) {
    results.value = [];
  } finally {
    loading.value = false;
  }
}
</script>
