<template>
  <aside class="w-[275px] shrink-0 hidden md:flex flex-col justify-between h-screen sticky top-0 px-3 py-4">
    <div>
      <AppLogo :size="44" />
      <nav class="mt-6 flex flex-col gap-1">
        <router-link to="/" class="flex items-center gap-4 px-3 py-3 rounded-full hover:bg-pond-surface font-bold">
          <Home :size="24" /> <span class="text-base">Feed</span>
        </router-link>

        <router-link
          to="/notifications"
          class="relative flex items-center gap-4 px-3 py-3 rounded-full hover:bg-pond-surface font-bold"
        >
          <Bell :size="24" />
          <span class="text-base">Notificacoes</span>
          <span
            v-if="notifications.unreadCount > 0"
            class="absolute left-6 top-1 bg-pond-red text-white text-[10px] font-bold rounded-full min-w-[16px] h-[16px] flex items-center justify-center px-1"
          >
            {{ notifications.unreadCount > 9 ? "9+" : notifications.unreadCount }}
          </span>
        </router-link>

        <router-link
          v-if="auth.user"
          :to="`/profile/${auth.user.handle}`"
          class="flex items-center gap-4 px-3 py-3 rounded-full hover:bg-pond-surface font-bold"
        >
          <User :size="24" /> <span class="text-base">Perfil</span>
        </router-link>
      </nav>

      <button
        v-if="showPostButton"
        @click="$emit('compose')"
        class="w-full mt-4 bg-pond-red hover:bg-red-600 transition-colors text-white font-bold py-3 rounded-full"
      >
        Postar
      </button>
    </div>

    <button
      @click="handleLogout"
      class="flex items-center gap-2 px-3 py-3 rounded-full hover:bg-pond-surface text-pond-muted text-sm"
    >
      <LogOut :size="18" /> Sair
    </button>
  </aside>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useNotificationsStore } from "../stores/notifications";
import AppLogo from "./AppLogo.vue";
import { Home, Bell, User, LogOut } from "lucide-vue-next";

defineProps({
  showPostButton: { type: Boolean, default: false },
});
defineEmits(["compose"]);

const auth = useAuthStore();
const notifications = useNotificationsStore();
const router = useRouter();

function handleLogout() {
  auth.logout();
  router.push("/login");
}

onMounted(() => {
  notifications.fetchUnreadCount();
});
</script>