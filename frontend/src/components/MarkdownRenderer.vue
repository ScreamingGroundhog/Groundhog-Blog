<template>
  <div class="prose max-w-none" ref="contentRef"></div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from "vue";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import katex from "katex";
import "highlight.js/styles/github-dark.css";
import "katex/dist/katex.min.css";

const props = defineProps({
  content: { type: String, default: "" },
});

const contentRef = ref(null);

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const md = new MarkdownIt({
  html: false,
  breaks: true,
  linkify: true,
  highlight: (code, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return (
          '<div class="code-block-wrapper"><button class="copy-btn" data-code="' +
          escapeHtml(code) +
          '">复制</button><pre class="hljs"><code>' +
          hljs.highlight(code, { language: lang }).value +
          "</code></pre></div>"
        );
      } catch {}
    }
    return (
      '<div class="code-block-wrapper"><button class="copy-btn" data-code="' +
      escapeHtml(code) +
      '">复制</button><pre class="hljs"><code>' +
      hljs.highlightAuto(code).value +
      "</code></pre></div>"
    );
  },
});

md.use((md) => {
  const defaultRender =
    md.renderer.rules.fence ||
    function (tokens, idx, options, env, self) {
      return self.renderToken(tokens, idx, options);
    };

  md.renderer.rules.fence = (tokens, idx, options, env, self) => {
    const token = tokens[idx];
    const code = token.content.trim();
    const lang = token.info.trim();
    if (lang === "math" || lang === "katex") {
      try {
        return `<div class="text-center my-4">${katex.renderToString(code, { displayMode: true, throwOnError: false })}</div>`;
      } catch {
        return `<pre><code>${escapeHtml(code)}</code></pre>`;
      }
    }
    return defaultRender(tokens, idx, options, env, self);
  };
});

md.use((md) => {
  md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
    tokens[idx].attrPush(["target", "_blank"]);
    tokens[idx].attrPush(["rel", "noopener noreferrer"]);
    return self.renderToken(tokens, idx, options);
  };
});

function renderMarkdown() {
  if (!contentRef.value) return;
  const html = md.render(props.content || "");
  contentRef.value.innerHTML = html;

  const copyBtns = contentRef.value.querySelectorAll(".copy-btn");
  copyBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const code = btn.getAttribute("data-code");
      navigator.clipboard.writeText(code).then(() => {
        btn.textContent = "已复制!";
        setTimeout(() => {
          btn.textContent = "复制";
        }, 2000);
      });
    });
  });

  const images = contentRef.value.querySelectorAll("img");
  images.forEach((img) => {
    img.addEventListener("click", () => {
      window.open(img.src, "_blank");
    });
  });
}

onMounted(() => {
  renderMarkdown();
});

watch(
  () => props.content,
  async () => {
    await nextTick();
    renderMarkdown();
  }
);
</script>
