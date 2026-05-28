<template>
  <footer class="border-t border-gray-800 py-8 mt-12">
    <div class="max-w-6xl mx-auto px-4 text-center text-gray-500 text-sm">
      <p>&copy; {{ year }} Blog. Powered by Vue + Flask.</p>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>
