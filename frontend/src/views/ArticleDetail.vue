<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <div v-if="loading" class="text-center text-gray-400 py-20">加载中...</div>
    <div v-else-if="error" class="text-center text-red-400 py-20">{{ error }}</div>
    <template v-else-if="article">
      <div class="flex gap-8">
        <article class="flex-1 min-w-0">
          <h1 class="text-3xl font-bold text-white mb-4">{{ article.title }}</h1>

          <div class="flex items-center gap-3 text-sm text-gray-400 mb-8">
            <span v-if="article.category" class="bg-gray-800 px-2 py-0.5 rounded">
              {{ article.category.name }}
            </span>
            <span>{{ formatDate(article.created_at) }}</span>
            <span>{{ article.view_count }} 次阅读</span>
          </div>

          <div v-if="article.tags.length" class="flex gap-2 mb-8">
            <span
              v-for="tag in article.tags"
              :key="tag.id"
              class="bg-gray-800 text-gray-300 px-2 py-0.5 rounded text-xs"
            >
              #{{ tag.name }}
            </span>
          </div>

          <MarkdownRenderer :content="article.content" />

          <div
            v-if="nearby.prev || nearby.next"
            class="flex justify-between mt-12 pt-8 border-t border-gray-800"
          >
            <router-link
              v-if="nearby.prev"
              :to="`/article/${nearby.prev.id}`"
              class="text-left max-w-[45%] group"
            >
              <span class="text-xs text-gray-500">上一篇</span>
              <p class="text-sm text-gray-300 group-hover:text-blue-400 transition-colors truncate">
                {{ nearby.prev.title }}
              </p>
            </router-link>
            <div v-else></div>
            <router-link
              v-if="nearby.next"
              :to="`/article/${nearby.next.id}`"
              class="text-right max-w-[45%] group"
            >
              <span class="text-xs text-gray-500">下一篇</span>
              <p class="text-sm text-gray-300 group-hover:text-blue-400 transition-colors truncate">
                {{ nearby.next.title }}
              </p>
            </router-link>
          </div>
        </article>

        <aside class="w-64 hidden lg:block shrink-0">
          <div class="sticky top-20">
            <TocNav :content="article.content" />
          </div>
        </aside>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import api from "../api";
import MarkdownRenderer from "../components/MarkdownRenderer.vue";
import TocNav from "../components/TocNav.vue";

const route = useRoute();
const article = ref(null);
const nearby = ref({ prev: null, next: null });
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

async function fetchArticle(id) {
  loading.value = true;
  error.value = "";
  try {
    const [articleRes, nearbyRes] = await Promise.all([
      api.get(`/public/articles/${id}`),
      api.get(`/public/articles/${id}/nearby`),
    ]);
    article.value = articleRes.data;
    nearby.value = nearbyRes.data;
  } catch (e) {
    error.value = "文章不存在或已删除";
  } finally {
    loading.value = false;
  }
}

onMounted(() => fetchArticle(route.params.id));
watch(() => route.params.id, (newId) => fetchArticle(newId));
</script>
