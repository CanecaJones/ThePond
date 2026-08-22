<template>
  <div class="min-h-screen bg-pond-black flex justify-center">
    <div class="flex w-full max-w-[990px]">
      <AppSidebar />

      <main class="w-full max-w-feed border-x border-pond-border min-h-screen">
        <header class="sticky top-0 bg-pond-black/80 backdrop-blur border-b border-pond-border px-4 py-3 z-10">
          <h1 class="text-xl font-bold">Notificacoes</h1>
        </header>

        <div v-if="loading" class="text-center text-pond-muted py-10">Carregando...</div>
        <div v-else>
          <p v-if="items.length === 0" class="text-center text-pond-muted py-10">
            Nenhuma notificacao ainda.
          </p>

          <router-link
            v-for="n in items"
            :key="n.id"
            :to="`/profile/${n.actor.handle}`"
            class="flex items-start gap-3 px-4 py-3 border-b border-pond-border hover:bg-pond-hover/50 transition-colors"
            :class="{ 'bg-pond-blue/5': !n.read }"
          >
            <component :is="iconFor(n.verb)" :size="20" class="text-pond-blue shrink-0 mt-1" />

            <div class="w-8 h-8 rounded-full bg-pond-surface flex items-center justify-center shrink-0 overflow-hidden">
              <img v-if="n.actor.avatar" :src="n.actor.avatar" class="w-full h-full object-cover" />
              <User v-else :size="16" class="text-pond-muted" />
            </div>

            <div>
              <p>
                <span class="font-bold">@{{ n.actor.handle }}</span>
                <span class="text-pond-muted"> {{ verbText(n.verb) }}</span>
              </p>
              <p class="text-pond-muted text-xs mt-0.5">{{ timeAgo(n.created_at) }}</p>
            </div>
          </router-link>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import AppSidebar from "../components/AppSidebar.vue";
import { useNotificationsStore } from "../stores/notifications";
import { Heart, Repeat2, UserPlus, User } from "lucide-vue-next";

const items = ref([]);
const loading = ref(true);
const notifications = useNotificationsStore();

function iconFor(verb) {
  if (verb === "like") return Heart;
  if (verb === "repost") return Repeat2;
  if (verb === "follow") return UserPlus;
  return User;
}

function verbText(verb) {
  if (verb === "like") return "curtiu seu post";
  if (verb === "repost") return "repostou seu post";
  if (verb === "follow") return "comecou a seguir voce";
  return "";
}

function timeAgo(dateStr) {
  const diff = (Date.now() - new Date(dateStr)) / 1000;
  if (diff < 60) return "agora";
  if (diff < 3600) return Math.floor(diff / 60) + "min";
  if (diff < 86400) return Math.floor(diff / 3600) + "h";
  return Math.floor(diff / 86400) + "d";
}

onMounted(async () => {
  const { data } = await api.get("/notifications/");
  items.value = data;
  loading.value = false;
  await notifications.markAllRead();
});
</script>