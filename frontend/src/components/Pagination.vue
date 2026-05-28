<template>
  <div class="pagination flex items-center justify-center gap-2 mt-8">
    <button
      :disabled="currentPage <= 1"
      @click="$emit('change', currentPage - 1)"
      class="px-3 py-1.5 rounded text-sm bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
    >
      上一页
    </button>
    <template v-for="p in pages" :key="p">
      <span
        v-if="p === '...'"
        class="px-2 text-gray-500"
      >...</span>
      <button
        v-else
        @click="$emit('change', p)"
        :class="[
          'px-3 py-1.5 rounded text-sm transition-colors',
          p === currentPage
            ? 'bg-blue-600 text-white'
            : 'bg-gray-800 text-gray-300 hover:bg-gray-700',
        ]"
      >
        {{ p }}
      </button>
    </template>
    <button
      :disabled="currentPage >= totalPages"
      @click="$emit('change', currentPage + 1)"
      class="px-3 py-1.5 rounded text-sm bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
    >
      下一页
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages: { type: Number, required: true },
});
defineEmits(["change"]);

const pages = computed(() => {
  const p = props.currentPage;
  const t = props.totalPages;
  if (t <= 7) return Array.from({ length: t }, (_, i) => i + 1);
  const pages = [];
  pages.push(1);
  if (p > 3) pages.push("...");
  for (let i = Math.max(2, p - 1); i <= Math.min(t - 1, p + 1); i++) pages.push(i);
  if (p < t - 2) pages.push("...");
  pages.push(t);
  return pages;
});
</script>
