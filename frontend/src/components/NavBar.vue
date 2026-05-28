<template>
  <nav class="sticky top-0 z-50 bg-gray-900/95 backdrop-blur border-b border-gray-800">
    <div class="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
      <router-link to="/" class="text-lg font-bold text-blue-400 hover:text-blue-300">
        &lt;Blog /&gt;
      </router-link>
      <div class="flex items-center gap-6 text-sm">
        <router-link to="/" class="text-gray-300 hover:text-white transition-colors">首页</router-link>
        <router-link to="/search" class="text-gray-300 hover:text-white transition-colors">搜索</router-link>
        <router-link to="/about" class="text-gray-300 hover:text-white transition-colors">关于</router-link>
        <router-link
          to="/admin"
          class="text-gray-500 hover:text-gray-300 transition-colors text-xs"
        >
          管理
        </router-link>
      </div>
    </div>
  </nav>
</template>
