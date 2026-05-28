<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-white">标签管理</h1>
      <button
        @click="showForm = true; editingTag = null; form.name = ''"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm transition-colors"
      >
        新建标签
      </button>
    </div>

    <div v-if="loading" class="text-center text-gray-400 py-10">加载中...</div>
    <div v-else-if="tags.length === 0" class="text-center text-gray-500 py-10">暂无标签</div>

    <div class="flex flex-wrap gap-3" v-else>
      <div
        v-for="tag in tags"
        :key="tag.id"
        class="bg-gray-900 rounded-lg px-4 py-3 border border-gray-800 flex items-center gap-3"
      >
        <span class="text-gray-100">#{{ tag.name }}</span>
        <span class="text-gray-500 text-xs">({{ tag.article_count }})</span>
        <button @click="editTag(tag)" class="text-blue-400 hover:text-blue-300 text-xs">编辑</button>
        <button @click="handleDelete(tag)" class="text-red-400 hover:text-red-300 text-xs">删除</button>
      </div>
    </div>

    <div
      v-if="showForm"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click.self="showForm = false"
    >
      <div class="bg-gray-900 rounded-lg p-6 border border-gray-800 w-full max-w-sm">
        <h3 class="text-lg font-semibold text-white mb-4">
          {{ editingTag ? "编辑标签" : "新建标签" }}
        </h3>
        <form @submit.prevent="handleSubmit" class="space-y-3">
          <input
            v-model="form.name"
            type="text"
            placeholder="标签名称"
            required
            class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-gray-100 text-sm focus:outline-none focus:border-blue-500 transition-colors"
          />
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

const tags = ref([]);
const loading = ref(true);
const showForm = ref(false);
const editingTag = ref(null);
const form = ref({ name: "" });

async function fetchTags() {
  loading.value = true;
  try {
    const { data } = await api.get("/tags");
    tags.value = data;
  } catch {}
  loading.value = false;
}

function editTag(tag) {
  editingTag.value = tag;
  form.value = { name: tag.name };
  showForm.value = true;
}

async function handleSubmit() {
  try {
    if (editingTag.value) {
      await api.put(`/tags/${editingTag.value.id}`, form.value);
    } else {
      await api.post("/tags", form.value);
    }
    showForm.value = false;
    fetchTags();
  } catch (e) {
    alert(e.response?.data?.error || "操作失败");
  }
}

async function handleDelete(tag) {
  if (!confirm(`确定删除标签「${tag.name}」?`)) return;
  try {
    await api.delete(`/tags/${tag.id}`);
    fetchTags();
  } catch {
    alert("删除失败");
  }
}

onMounted(() => fetchTags());
</script>
