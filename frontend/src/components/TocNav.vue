<template>
  <div v-if="tocItems.length > 0" class="article-toc bg-gray-900 rounded-lg p-4">
    <h4 class="text-gray-300 font-semibold mb-2">目录</h4>
    <nav>
      <a
        v-for="(item, idx) in tocItems"
        :key="idx"
        :href="`#${item.id}`"
        :class="['toc-item', `toc-${item.level}`]"
      >
        {{ item.text }}
      </a>
    </nav>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  content: { type: String, default: "" },
});

const tocItems = computed(() => {
  const items = [];
  const regex = /^(#{1,4})\s+(.+)$/gm;
  let match;
  while ((match = regex.exec(props.content)) !== null) {
    items.push({
      level: "h" + match[1].length,
      text: match[2].trim(),
      id: match[2]
        .trim()
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fff]+/g, "-")
        .replace(/(^-|-$)/g, ""),
    });
  }
  return items;
});
</script>
