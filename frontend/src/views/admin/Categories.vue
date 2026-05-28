<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-white">分类管理</h1>
      <button
        @click="showForm = true; editingCategory = null; form = { name: '', description: '' }"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm transition-colors"
      >
        新建分类
      </button>
    </div>

    <div v-if="loading" class="text-center text-gray-400 py-10">加载中...</div>
    <div v-else-if="categories.length === 0" class="text-center text-gray-500 py-10">暂无分类</div>

    <div class="grid gap-3" v-else>
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="bg-gray-900 rounded-lg p-4 border border-gray-800 flex items-center justify-between"
      >
        <div>
          <p class="text-gray-100 font-medium">{{ cat.name }}</p>
          <p class="text-gray-500 text-xs mt-1">{{ cat.article_count }} 篇文章</p>
        </div>
        <div class="flex gap-2">
          <button
            @click="editCategory(cat)"
            class="text-blue-400 hover:text-blue-300 text-xs"
          >
            编辑
          </button>
          <button
            @click="handleDelete(cat)"
            class="text-red-400 hover:text-red-300 text-xs"
          >
            删除
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showForm"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click.self="showForm = false"
    >
      <div class="bg-gray-900 rounded-lg p-6 border border-gray-800 w-full max-w-md">
        <h3 class="text-lg font-semibold text-white mb-4">
          {{ editingCategory ? "编辑分类" : "新建分类" }}
        </h3>
        <form @submit.prevent="handleSubmit" class="space-y-3">
          <input
            v-model="form.name"
            type="text"
            placeholder="分类名称"
            required
            class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-gray-100 text-sm focus:outline-none focus:border-blue-500 transition-colors"
          />
          <textarea
            v-model="form.description"
            placeholder="分类描述（可选）"
            rows="2"
            class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-gray-100 text-sm focus:outline-none focus:border-blue-500 transition-colors resize-none"
          ></textarea>
          <div class="flex justify-end gap-2 pt-2">
            <button
              type="button"
              @click="showForm = false"
              class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded text-sm transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm transition-colors"
            >
              保存
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../api";

const categories = ref([]);
const loading = ref(true);
const showForm = ref(false);
const editingCategory = ref(null);
const form = ref({ name: "", description: "" });

async function fetchCategories() {
  loading.value = true;
  try {
    const { data } = await api.get("/categories");
    categories.value = data;
  } catch {}
  loading.value = false;
}

function editCategory(cat) {
  editingCategory.value = cat;
  form.value = { name: cat.name, description: cat.description || "" };
  showForm.value = true;
}

async function handleSubmit() {
  try {
    if (editingCategory.value) {
      await api.put(`/categories/${editingCategory.value.id}`, form.value);
    } else {
      await api.post("/categories", form.value);
    }
    showForm.value = false;
    fetchCategories();
  } catch (e) {
    alert(e.response?.data?.error || "操作失败");
  }
}

async function handleDelete(cat) {
  if (!confirm(`确定删除分类「${cat.name}」?`)) return;
  try {
    await api.delete(`/categories/${cat.id}`);
    fetchCategories();
  } catch {
    alert("删除失败");
  }
}

onMounted(() => fetchCategories());
</script>
