<template>
  <div class="min-h-screen flex">
    <aside class="w-56 bg-gray-900 border-r border-gray-800 shrink-0 min-h-screen">
      <div class="p-4 border-b border-gray-800">
        <router-link to="/admin" class="text-lg font-bold text-blue-400">
          管理后台
        </router-link>
      </div>
      <nav class="p-3 space-y-1">
        <router-link
          to="/admin/articles"
          class="flex items-center gap-2 px-3 py-2 rounded text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          active-class="bg-gray-800 text-white"
        >
          文章管理
        </router-link>
        <router-link
          to="/admin/categories"
          class="flex items-center gap-2 px-3 py-2 rounded text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          active-class="bg-gray-800 text-white"
        >
          分类管理
        </router-link>
        <router-link
          to="/admin/tags"
          class="flex items-center gap-2 px-3 py-2 rounded text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          active-class="bg-gray-800 text-white"
        >
          标签管理
        </router-link>
        <router-link
          to="/admin/files"
          class="flex items-center gap-2 px-3 py-2 rounded text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          active-class="bg-gray-800 text-white"
        >
          文件管理
        </router-link>
        <router-link
          to="/admin/settings"
          class="flex items-center gap-2 px-3 py-2 rounded text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          active-class="bg-gray-800 text-white"
        >
          个人设置
        </router-link>
        <div class="border-t border-gray-800 my-2"></div>
        <router-link
          to="/"
          class="flex items-center gap-2 px-3 py-2 rounded text-sm text-gray-500 hover:text-gray-300 transition-colors"
        >
          返回前台
        </router-link>
        <button
          @click="handleLogout"
          class="flex items-center gap-2 px-3 py-2 rounded text-sm text-gray-500 hover:text-red-400 transition-colors w-full text-left"
        >
          退出登录
        </button>
      </nav>
    </aside>
    <main class="flex-1 p-6 min-w-0">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const auth = useAuthStore();

function handleLogout() {
  auth.logout();
  router.push("/admin/login");
}

onMounted(async () => {
  if (!auth.isLoggedIn) {
    router.push("/admin/login");
    return;
  }
  try {
    await auth.fetchMe();
  } catch {
    auth.logout();
    router.push("/admin/login");
  }
});
</script>
