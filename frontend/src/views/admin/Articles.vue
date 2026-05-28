<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-white">文章管理</h1>
      <router-link
        to="/admin/articles/new"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm transition-colors"
      >
        新建文章
      </router-link>
    </div>

    <div class="flex items-center gap-3 mb-4 flex-wrap">
      <select
        v-model="statusFilter"
        @change="fetchArticles(1)"
        class="bg-gray-800 text-gray-300 px-3 py-1.5 rounded text-sm border border-gray-700 focus:outline-none"
      >
        <option value="">全部状态</option>
        <option value="published">已发布</option>
        <option value="draft">草稿</option>
        <option value="hidden">已隐藏</option>
      </select>
    </div>

    <div v-if="loading" class="text-center text-gray-400 py-10">加载中...</div>
    <div v-else-if="articles.length === 0" class="text-center text-gray-500 py-10">暂无文章</div>

    <div class="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden" v-else>
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-800 text-gray-400">
            <th class="text-left px-4 py-3 font-medium">标题</th>
            <th class="text-left px-4 py-3 font-medium">状态</th>
            <th class="text-left px-4 py-3 font-medium hidden md:table-cell">分类</th>
            <th class="text-left px-4 py-3 font-medium hidden md:table-cell">时间</th>
            <th class="text-right px-4 py-3 font-medium">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="article in articles"
            :key="article.id"
            class="border-b border-gray-800/50 hover:bg-gray-800/50 transition-colors"
          >
            <td class="px-4 py-3">
              <span class="text-gray-100">{{ article.title }}</span>
              <span v-if="article.is_pinned" class="ml-2 text-xs text-blue-400">置顶</span>
            </td>
            <td class="px-4 py-3">
              <span
                :class="{
                  'text-green-400': article.status === 'published',
                  'text-yellow-400': article.status === 'draft',
                  'text-gray-500': article.status === 'hidden',
                }"
              >
                {{ statusLabel(article.status) }}
              </span>
            </td>
            <td class="px-4 py-3 text-gray-400 hidden md:table-cell">
              {{ article.category?.name || "-" }}
            </td>
            <td class="px-4 py-3 text-gray-400 hidden md:table-cell">
              {{ formatDate(article.created_at) }}
            </td>
            <td class="px-4 py-3 text-right">
              <router-link
                :to="`/admin/articles/${article.id}/edit`"
                class="text-blue-400 hover:text-blue-300 text-xs mr-2"
              >
                编辑
              </router-link>
              <button
                @click="handleDelete(article)"
                class="text-red-400 hover:text-red-300 text-xs"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pagination
      v-if="totalPages > 1"
      :current-page="currentPage"
      :total-pages="totalPages"
      @change="fetchArticles"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../api";
import Pagination from "../../components/Pagination.vue";

const articles = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const loading = ref(true);
const statusFilter = ref("");

function statusLabel(s) {
  return { published: "已发布", draft: "草稿", hidden: "已隐藏" }[s] || s;
}
function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("zh-CN");
}

async function fetchArticles(page = 1) {
  loading.value = true;
  try {
    const params = { page, per_page: 15 };
    if (statusFilter.value) params.status = statusFilter.value;
    const { data } = await api.get("/articles", { params });
    articles.value = data.items;
    currentPage.value = data.page;
    totalPages.value = data.pages;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function handleDelete(article) {
  if (!confirm(`确定删除「${article.title}」?`)) return;
  try {
    await api.delete(`/articles/${article.id}`);
    fetchArticles(currentPage.value);
  } catch (e) {
    alert("删除失败");
  }
}

onMounted(() => fetchArticles());
</script>
