import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/article/:id",
    name: "Article",
    component: () => import("../views/ArticleDetail.vue"),
  },
  {
    path: "/search",
    name: "Search",
    component: () => import("../views/Search.vue"),
  },
  {
    path: "/about",
    name: "About",
    component: () => import("../views/About.vue"),
  },
  {
    path: "/admin/login",
    name: "AdminLogin",
    component: () => import("../views/admin/Login.vue"),
  },
  {
    path: "/admin",
    name: "Admin",
    component: () => import("../views/admin/Admin.vue"),
    children: [
      {
        path: "",
        redirect: "/admin/articles",
      },
      {
        path: "articles",
        name: "AdminArticles",
        component: () => import("../views/admin/Articles.vue"),
      },
      {
        path: "articles/new",
        name: "AdminArticleNew",
        component: () => import("../views/admin/ArticleEditor.vue"),
      },
      {
        path: "articles/:id/edit",
        name: "AdminArticleEdit",
        component: () => import("../views/admin/ArticleEditor.vue"),
      },
      {
        path: "categories",
        name: "AdminCategories",
        component: () => import("../views/admin/Categories.vue"),
      },
      {
        path: "tags",
        name: "AdminTags",
        component: () => import("../views/admin/Tags.vue"),
      },
      {
        path: "files",
        name: "AdminFiles",
        component: () => import("../views/admin/Files.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
