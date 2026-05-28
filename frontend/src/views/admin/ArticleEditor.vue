<template>
  <div class="max-w-4xl">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-white">
        {{ isEdit ? "编辑文章" : "新建文章" }}
      </h1>
      <div class="flex gap-2">
        <button
          @click="saveDraft"
          :disabled="saving"
          class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded text-sm transition-colors disabled:opacity-50"
        >
          存草稿
        </button>
        <button
          @click="publish"
          :disabled="saving"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm transition-colors disabled:opacity-50"
        >
          {{ saving ? "保存中..." : "发布" }}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-4">
        <input
          v-model="form.title"
          type="text"
          placeholder="文章标题"
          class="w-full bg-gray-900 border border-gray-700 rounded px-4 py-2.5 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
        />

        <div class="flex gap-2">
          <button
            @click="insertMarkdown('**', '**')"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="加粗"
          >B</button>
          <button
            @click="insertMarkdown('*', '*')"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="斜体"
          >I</button>
          <button
            @click="insertMarkdown('~~', '~~')"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="删除线"
          >S</button>
          <button
            @click="insertMarkdown('\n```\n', '\n```\n')"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="代码块"
          >&lt;/&gt;</button>
          <button
            @click="insertMarkdown('[', '](url)')"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="链接"
          >🔗</button>
          <button
            @click="insertMarkdown('![', '](url)')"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="图片"
          >🖼</button>
          <button
            @click="insertMarkdown('\n> ', '')"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="引用"
          >"</button>
          <button
            @click="triggerFileUpload"
            class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs transition-colors"
            title="上传图片"
          >📤</button>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleFileUpload"
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-gray-500 mb-1">编辑 (Markdown)</label>
            <textarea
              v-model="form.content"
              class="w-full bg-gray-900 border border-gray-700 rounded p-4 text-gray-100 font-mono text-sm resize-y min-h-[400px] focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="在此输入 Markdown 内容..."
              @scroll="syncScroll"
              ref="editorRef"
            ></textarea>
          </div>
          <div>
            <label class="block text-xs text-gray-500 mb-1">预览</label>
            <div
              class="bg-gray-900 border border-gray-700 rounded p-4 min-h-[400px] overflow-y-auto"
              ref="previewRef"
            >
              <MarkdownRenderer :content="form.content" />
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-4">
        <div class="bg-gray-900 rounded-lg p-4 border border-gray-800 space-y-3">
          <h3 class="text-sm font-semibold text-gray-300">发布设置</h3>

          <div>
            <label class="block text-xs text-gray-500 mb-1">摘要</label>
            <textarea
              v-model="form.summary"
              rows="3"
              class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-gray-100 text-sm focus:outline-none focus:border-blue-500 transition-colors resize-none"
              placeholder="文章摘要..."
            ></textarea>
          </div>

          <div>
            <label class="block text-xs text-gray-500 mb-1">分类</label>
            <select
              v-model="form.category_id"
              class="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-gray-100 text-sm focus:outline-none focus:border-blue-500 transition-colors"
            >
              <option :value="null">无分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-xs text-gray-500 mb-1">标签</label>
            <div class="flex flex-wrap gap-2">
              <label
                v-for="tag in tags"
                :key="tag.id"
                class="flex items-center gap-1 text-xs text-gray-400 cursor-pointer"
              >
                <input
                  type="checkbox"
                  :value="tag.id"
                  v-model="form.tag_ids"
                  class="rounded bg-gray-800 border-gray-600"
                />
                {{ tag.name }}
              </label>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <input
              type="checkbox"
              v-model="form.is_pinned"
              class="rounded bg-gray-800 border-gray-600"
            />
            <label class="text-xs text-gray-400">置顶文章</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../../api";
import MarkdownRenderer from "../../components/MarkdownRenderer.vue";

const route = useRoute();
const router = useRouter();
const isEdit = computed(() => !!route.params.id);

const form = ref({
  title: "",
  content: "",
  summary: "",
  category_id: null,
  tag_ids: [],
  is_pinned: false,
});
const categories = ref([]);
const tags = ref([]);
const saving = ref(false);
const editorRef = ref(null);
const previewRef = ref(null);
const fileInput = ref(null);

function insertMarkdown(before, after) {
  const el = document.querySelector("textarea");
  if (!el) return;
  const start = el.selectionStart;
  const end = el.selectionEnd;
  const text = form.value.content;
  form.value.content =
    text.substring(0, start) + before + text.substring(start, end) + after + text.substring(end);
}

function triggerFileUpload() {
  fileInput.value?.click();
}

async function handleFileUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
  try {
    const { data } = await api.post("/files", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    insertMarkdown("![", `](${data.url})`);
  } catch {
    alert("上传失败");
  }
}

function syncScroll() {
  if (!editorRef.value || !previewRef.value) return;
  const ratio =
    editorRef.value.scrollTop /
    (editorRef.value.scrollHeight - editorRef.value.clientHeight);
  previewRef.value.scrollTop =
    ratio * (previewRef.value.scrollHeight - previewRef.value.clientHeight);
}

async function fetchFormData() {
  const [catRes, tagRes] = await Promise.all([
    api.get("/categories"),
    api.get("/tags"),
  ]);
  categories.value = catRes.data;
  tags.value = tagRes.data;
}

async function fetchArticle() {
  const { data } = await api.get(`/articles/${route.params.id}`);
  form.value = {
    title: data.title,
    content: data.content,
    summary: data.summary,
    category_id: data.category?.id || null,
    tag_ids: data.tags?.map((t) => t.id) || [],
    is_pinned: data.is_pinned,
  };
}

async function saveDraft() {
  saving.value = true;
  try {
    const payload = { ...form.value, status: "draft" };
    if (isEdit.value) {
      await api.put(`/articles/${route.params.id}`, payload);
    } else {
      await api.post("/articles", payload);
    }
    router.push("/admin/articles");
  } catch (e) {
    alert(e.response?.data?.error || "保存失败");
  } finally {
    saving.value = false;
  }
}

async function publish() {
  if (!form.value.title.trim()) {
    alert("标题不能为空");
    return;
  }
  saving.value = true;
  try {
    const payload = { ...form.value, status: "published" };
    if (isEdit.value) {
      await api.put(`/articles/${route.params.id}`, payload);
    } else {
      await api.post("/articles", payload);
    }
    router.push("/admin/articles");
  } catch (e) {
    alert(e.response?.data?.error || "发布失败");
  } finally {
    saving.value = false;
  }
}

onMounted(async () => {
  await fetchFormData();
  if (isEdit.value) {
    await fetchArticle();
  }
});
</script>
