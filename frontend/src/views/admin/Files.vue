<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-white">文件管理</h1>
      <label class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm cursor-pointer transition-colors">
        上传文件
        <input type="file" accept="image/*" class="hidden" @change="handleUpload" />
      </label>
    </div>

    <div v-if="uploading" class="text-center text-gray-400 py-4">上传中...</div>

    <div v-if="files.length === 0 && !uploading" class="text-center text-gray-500 py-10">
      暂无上传的文件
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4" v-else>
      <div
        v-for="file in files"
        :key="file"
        class="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden"
      >
        <img :src="`/api/files/${file}`" :alt="file" class="w-full h-32 object-cover" />
        <div class="p-2">
          <p class="text-xs text-gray-400 truncate" :title="file">{{ file }}</p>
          <button @click="copyUrl(file)" class="text-blue-400 hover:text-blue-300 text-xs mt-1">
            复制链接
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../api";

const files = ref([]);
const uploading = ref(false);

async function fetchFiles() {
  try {
    const { data } = await api.get("/files/list");
    files.value = data;
  } catch {}
}

async function handleUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  uploading.value = true;
  try {
    const formData = new FormData();
    formData.append("file", file);
    await api.post("/files", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    await fetchFiles();
  } catch {
    alert("上传失败");
  } finally {
    uploading.value = false;
  }
}

function copyUrl(filename) {
  const url = `${window.location.origin}/api/files/${filename}`;
  navigator.clipboard.writeText(url).then(() => {
    alert("链接已复制");
  });
}

onMounted(() => fetchFiles());
</script>
