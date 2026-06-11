<template>
  <div class="max-w-lg">
    <h1 class="text-xl font-bold text-white mb-6">个人设置</h1>

    <!-- Nickname -->
    <div class="mb-6">
      <label class="block text-sm text-gray-400 mb-2">昵称</label>
      <input
        v-model="nickname"
        class="w-full bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
      />
    </div>

    <!-- Description -->
    <div class="mb-6">
      <label class="block text-sm text-gray-400 mb-2">个人简介</label>
      <textarea
        v-model="description"
        rows="3"
        placeholder="一句话介绍自己..."
        class="w-full bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 resize-none"
      ></textarea>
    </div>

    <!-- Avatar -->
    <div class="mb-6">
      <label class="block text-sm text-gray-400 mb-2">头像</label>
      <div class="flex items-center gap-3 mb-2">
        <img v-if="avatar" :src="avatar" class="w-12 h-12 rounded-full object-cover border border-gray-700" />
        <div v-else class="w-12 h-12 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center text-gray-500 text-xs">无</div>
      </div>
      <label class="inline-block bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded text-xs cursor-pointer transition-colors">
        上传新头像
        <input type="file" accept="image/*" class="hidden" @change="handleAvatarUpload" />
      </label>
    </div>

    <!-- Password -->
    <div class="mb-6 p-4 bg-gray-900 rounded-lg border border-gray-800">
      <h2 class="text-sm font-semibold text-white mb-3">修改密码</h2>

      <div class="mb-3">
        <label class="block text-xs text-gray-500 mb-1">原密码</label>
        <input
          v-model="oldPassword"
          type="password"
          class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
        />
      </div>

      <div class="mb-3">
        <label class="block text-xs text-gray-500 mb-1">新密码</label>
        <input
          v-model="newPassword"
          type="password"
          class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
        />
      </div>

      <div class="mb-3">
        <label class="block text-xs text-gray-500 mb-1">确认新密码</label>
        <input
          v-model="confirmPassword"
          type="password"
          class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
        />
      </div>
    </div>

    <button
      @click="save"
      :disabled="saving"
      class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 text-white px-6 py-2 rounded text-sm transition-colors"
    >
      {{ saving ? "保存中..." : "保存设置" }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../api";
import { useAuthStore } from "../../stores/auth";

const auth = useAuthStore();
const nickname = ref("");
const avatar = ref("");
const description = ref("");
const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const saving = ref(false);

function showToast(msg) {
  const el = document.createElement("div");
  el.textContent = msg;
  el.className = "fixed top-4 right-4 z-50 bg-gray-800 border border-gray-700 text-white px-4 py-2 rounded text-sm shadow-lg";
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2500);
}

onMounted(() => {
  nickname.value = auth.user?.nickname || "";
  avatar.value = auth.user?.avatar || "";
  description.value = auth.user?.description || "";
});

async function handleAvatarUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
  try {
    const { data } = await api.post("/files", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    avatar.value = data.url;
  } catch {
    showToast("头像上传失败");
  }
}

async function save() {
  saving.value = true;
  try {
    const payload = { nickname: nickname.value, avatar: avatar.value, description: description.value };

    if (newPassword.value) {
      if (!oldPassword.value) {
        showToast("请输入原密码");
        saving.value = false;
        return;
      }
      if (newPassword.value.length < 6) {
        showToast("新密码长度不能少于6位");
        saving.value = false;
        return;
      }
      if (newPassword.value !== confirmPassword.value) {
        showToast("两次输入的新密码不一致");
        saving.value = false;
        return;
      }
      payload.old_password = oldPassword.value;
      payload.new_password = newPassword.value;
    }

    const { data } = await api.put("/auth/me", payload);
    auth.user = data;
    oldPassword.value = "";
    newPassword.value = "";
    confirmPassword.value = "";
    showToast("设置已保存");
  } catch (e) {
    showToast(e.response?.data?.error || "保存失败");
  } finally {
    saving.value = false;
  }
}
</script>
