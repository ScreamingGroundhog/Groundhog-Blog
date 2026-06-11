<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-white">文件管理</h1>
      <label class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm cursor-pointer transition-colors">
        上传文件
        <input type="file" accept="image/*" class="hidden" @change="onFilePicked" />
      </label>
    </div>

    <!-- Inline upload confirmation -->
    <div v-if="pendingFile" class="mb-6 bg-gray-900 border border-gray-800 rounded-lg p-4 flex items-center gap-3">
      <span class="text-sm text-gray-400 whitespace-nowrap">文件名:</span>
      <input
        v-model="customName"
        class="flex-1 bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-sm text-white focus:outline-none focus:border-blue-500"
      />
      <span class="text-xs text-gray-500">.{{ pendingExt }}</span>
      <button @click="doUpload" class="px-4 py-1.5 text-sm text-white bg-blue-600 hover:bg-blue-500 rounded transition-colors">确认上传</button>
      <button @click="cancelUpload" class="px-4 py-1.5 text-sm text-gray-400 hover:text-white transition-colors">取消</button>
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
          <div class="flex items-center justify-between mt-1">
            <button @click="copyUrl(file)" class="text-blue-400 hover:text-blue-300 text-xs">
              复制链接
            </button>
            <button @click="confirmDelete(file)" class="text-red-400 hover:text-red-300 text-xs">
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <div v-if="showConfirm" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black/60" @click="showConfirm = false"></div>
      <div class="relative bg-gray-800 rounded-lg border border-gray-700 p-6 w-80 shadow-xl">
        <p class="text-white text-sm mb-4">{{ confirmMessage }}</p>
        <div class="flex justify-end gap-3">
          <button @click="showConfirm = false" class="px-4 py-1.5 text-sm text-gray-300 bg-gray-700 hover:bg-gray-600 rounded transition-colors">取消</button>
          <button @click="doDelete" class="px-4 py-1.5 text-sm text-white bg-red-600 hover:bg-red-500 rounded transition-colors">删除</button>
        </div>
      </div>
    </div>

    <!-- Toast notification -->
    <div v-if="toast" class="fixed top-4 right-4 z-50 bg-gray-800 border border-gray-700 text-white px-4 py-2 rounded text-sm shadow-lg transition-opacity">
      {{ toast }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../../api";
import { useAuthStore } from "../../stores/auth";

const auth = useAuthStore();

const avatarFilename = computed(() => {
  const avatar = auth.user?.avatar || "";
  if (avatar.startsWith("/api/files/")) {
    return avatar.split("/").pop();
  }
  return "";
});

const allFiles = ref([]);
const files = computed(() => {
  return allFiles.value.filter(f => f !== avatarFilename.value);
});
const uploading = ref(false);
const pendingFile = ref(null);
const customName = ref("");
const pendingExt = ref("");
const showConfirm = ref(false);
const confirmMessage = ref("");
const pendingDeleteFile = ref(null);
const toast = ref("");

function showToast(msg) {
  toast.value = msg;
  setTimeout(() => { toast.value = ""; }, 2500);
}

async function fetchFiles() {
  try {
    const { data } = await api.get("/files/list");
    allFiles.value = data;
  } catch {}
}

function onFilePicked(e) {
  const file = e.target.files[0];
  if (!file) return;
  pendingFile.value = file;
  const dotIndex = file.name.lastIndexOf(".");
  if (dotIndex > 0) {
    customName.value = file.name.substring(0, dotIndex);
    pendingExt.value = file.name.substring(dotIndex + 1);
  } else {
    customName.value = file.name;
    pendingExt.value = "";
  }
  // Reset the input so re-selecting the same file triggers change again
  e.target.value = "";
}

function cancelUpload() {
  pendingFile.value = null;
  customName.value = "";
  pendingExt.value = "";
}

async function doUpload() {
  if (!pendingFile.value) return;
  uploading.value = true;
  try {
    const formData = new FormData();
    formData.append("file", pendingFile.value);
    const name = customName.value.trim();
    if (name) {
      formData.append("name", name);
    }
    await api.post("/files", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    cancelUpload();
    await fetchFiles();
  } catch {
    showToast("上传失败");
  } finally {
    uploading.value = false;
  }
}

function confirmDelete(filename) {
  pendingDeleteFile.value = filename;
  confirmMessage.value = `确定要删除 ${filename} 吗？`;
  showConfirm.value = true;
}

async function doDelete() {
  showConfirm.value = false;
  const filename = pendingDeleteFile.value;
  pendingDeleteFile.value = null;
  if (!filename) return;
  try {
    await api.delete(`/files/${filename}`);
    await fetchFiles();
  } catch {
    showToast("删除失败");
  }
}

function copyUrl(filename) {
  const url = `${window.location.origin}/api/files/${filename}`;
  navigator.clipboard.writeText(url).then(() => {
    showToast("链接已复制");
  });
}

onMounted(async () => {
  if (auth.token && !auth.user) {
    try { await auth.fetchMe(); } catch {}
  }
  fetchFiles();
});
</script>
