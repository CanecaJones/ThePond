import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import FeedView from "../views/FeedView.vue";

const routes = [
  { path: "/login", name: "login", component: LoginView },
  { path: "/register", name: "register", component: RegisterView },
  { path: "/", name: "feed", component: FeedView, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login" };
  }
});

export default router;