<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <div v-if="loading" class="text-center text-gray-400 py-20">加载中...</div>
    <div v-else-if="error" class="text-center text-red-400 py-20">{{ error }}</div>
    <template v-else>
      <div class="mb-6 flex items-center gap-4 flex-wrap">
        <select
          v-model="selectedCategory"
          @change="fetchArticles(1)"
          class="bg-gray-800 text-gray-300 px-3 py-1.5 rounded text-sm border border-gray-700 focus:outline-none"
        >
          <option value="">全部分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
        <select
          v-model="selectedTag"
          @change="fetchArticles(1)"
          class="bg-gray-800 text-gray-300 px-3 py-1.5 rounded text-sm border border-gray-700 focus:outline-none"
        >
          <option value="">全部标签</option>
          <option v-for="tag in tags" :key="tag.id" :value="tag.id">
            {{ tag.name }}
          </option>
        </select>
      </div>

      <div v-if="articles.length === 0" class="text-center text-gray-500 py-20">
        暂无文章
      </div>

      <div class="space-y-6">
        <article
          v-for="article in articles"
          :key="article.id"
          class="bg-gray-900 rounded-lg p-6 border border-gray-800 hover:border-gray-700 transition-colors"
          :class="{ 'border-blue-500/50': article.is_pinned }"
        >
          <div class="flex items-center gap-2 text-xs text-gray-500 mb-2">
            <span v-if="article.is_pinned" class="text-blue-400 font-semibold">置顶</span>
            <span v-if="article.category" class="bg-gray-800 px-2 py-0.5 rounded">
              {{ article.category.name }}
            </span>
            <span>{{ formatDate(article.created_at) }}</span>
          </div>
          <router-link
            :to="`/article/${article.id}`"
            class="text-xl font-bold text-white hover:text-blue-400 transition-colors block mb-2"
          >
            {{ article.title }}
          </router-link>
          <p class="text-gray-400 text-sm line-clamp-2 mb-3">{{ article.summary }}</p>
          <div class="flex items-center gap-3 text-xs text-gray-500">
            <span class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              {{ article.view_count }}
            </span>
            <div class="flex gap-1" v-if="article.tags.length">
              <span
                v-for="tag in article.tags"
                :key="tag.id"
                class="bg-gray-800 px-2 py-0.5 rounded hover:bg-gray-700 cursor-pointer transition-colors"
              >
                #{{ tag.name }}
              </span>
            </div>
          </div>
        </article>
      </div>

      <Pagination
        v-if="totalPages > 1"
        :current-page="currentPage"
        :total-pages="totalPages"
        @change="fetchArticles"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";
import Pagination from "../components/Pagination.vue";

const articles = ref([]);
const categories = ref([]);
const tags = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const selectedCategory = ref("");
const selectedTag = ref("");
const loading = ref(true);
const error = ref("");

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

async function fetchArticles(page = 1) {
  loading.value = true;
  error.value = "";
  try {
    const params = { page, per_page: 10 };
    if (selectedCategory.value) params.category_id = selectedCategory.value;
    if (selectedTag.value) params.tag_id = selectedTag.value;
    const { data } = await api.get("/public/articles", { params });
    articles.value = data.items;
    currentPage.value = data.page;
    totalPages.value = data.pages;
  } catch (e) {
    error.value = "加载失败，请稍后重试";
  } finally {
    loading.value = false;
  }
}

async function fetchFilters() {
  try {
    const [catRes, tagRes] = await Promise.all([
      api.get("/public/categories"),
      api.get("/public/tags"),
    ]);
    categories.value = catRes.data;
    tags.value = tagRes.data;
  } catch {}
}

onMounted(() => {
  fetchArticles();
  fetchFilters();
});
</script>
