<template>
  <div class="min-h-screen bg-pond-black flex justify-center">
    <div class="flex w-full max-w-[990px]">
      <AppSidebar />

      <main class="w-full max-w-feed border-x border-pond-border min-h-screen">
        <header class="sticky top-0 bg-pond-black/80 backdrop-blur border-b border-pond-border px-4 py-3 z-10 flex items-center gap-4">
          <router-link to="/" class="text-pond-muted hover:text-pond-text">
            <ArrowLeft :size="20" />
          </router-link>
          <h1 class="text-lg font-bold">{{ profile?.username || "Perfil" }}</h1>
        </header>

        <div v-if="loading" class="text-center text-pond-muted py-10">Carregando perfil...</div>

        <div v-else-if="profile">
          <div class="h-32 bg-gradient-to-r from-pond-blue/30 to-pond-black"></div>

          <div class="px-4 -mt-12">
            <div class="w-24 h-24 rounded-full bg-pond-surface border-4 border-pond-black overflow-hidden flex items-center justify-center">
              <img v-if="profile.avatar" :src="profile.avatar" class="w-full h-full object-cover" />
              <User v-else :size="36" class="text-pond-muted" />
            </div>

            <div class="mt-3 flex items-start justify-between">
              <div>
                <h2 class="text-xl font-bold">{{ profile.username }}</h2>
                <p class="text-pond-muted">@{{ profile.handle }}</p>
              </div>

              <label
                v-if="isOwnProfile"
                class="border border-pond-border rounded-full px-4 py-1.5 text-sm font-bold cursor-pointer hover:bg-pond-surface"
              >
                Trocar foto
                <input type="file" accept="image/*" @change="onAvatarChange" hidden />
              </label>
            </div>

            <p v-if="profile.bio" class="mt-3 whitespace-pre-wrap">{{ profile.bio }}</p>

            <div v-if="isOwnProfile" class="mt-3">
              <textarea
                v-model="bioDraft"
                maxlength="160"
                placeholder="Escreva uma bio..."
                rows="2"
                class="w-full bg-pond-surface border border-pond-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-pond-blue"
              ></textarea>
              <button
                @click="saveBio"
                class="mt-2 bg-pond-red hover:bg-red-600 transition-colors text-white text-sm font-bold px-4 py-1.5 rounded-full"
              >
                Salvar bio
              </button>
            </div>

            <div class="flex gap-4 mt-4 text-sm">
              <span><strong>{{ profile.following_count }}</strong> <span class="text-pond-muted">seguindo</span></span>
              <span><strong>{{ profile.followers_count }}</strong> <span class="text-pond-muted">seguidores</span></span>
            </div>
          </div>

          <div class="border-t border-pond-border mt-4">
            <PostCard
              v-for="post in posts"
              :key="post.id"
              :post="post"
              @like="toggleLike"
              @repost="toggleRepost"
            />
            <p v-if="posts.length === 0" class="text-center text-pond-muted py-10">Nenhum post ainda.</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import api from "../services/api";
import AppSidebar from "../components/AppSidebar.vue";
import PostCard from "../components/PostCard.vue";
import { User, ArrowLeft } from "lucide-vue-next";


const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const profile = ref(null);
const posts = ref([]);
const loading = ref(true);
const bioDraft = ref("");

const isOwnProfile = computed(() => auth.user && profile.value && auth.user.handle === profile.value.handle);

async function loadProfile() {
  loading.value = true;
  const handle = route.params.handle;
  const { data } = await api.get(`/auth/profile/${handle}/`);
  profile.value = data;
  bioDraft.value = data.bio || "";

  const postsRes = await api.get(`/posts/user/${handle}/`);
  posts.value = postsRes.data;

  loading.value = false;
}

async function onAvatarChange(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("avatar", file);

  const { data } = await api.patch("/auth/me/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  profile.value.avatar = data.avatar;
  auth.user.avatar = data.avatar;
}

async function saveBio() {
  const { data } = await api.patch("/auth/me/", { bio: bioDraft.value });
  profile.value.bio = data.bio;
}

async function toggleLike(post) {
  const { data } = await api.post(`/posts/${post.id}/like/`);
  post.liked_by_me = data.liked;
  post.likes_count += data.liked ? 1 : -1;
}

async function toggleRepost(post) {
  const { data } = await api.post(`/posts/${post.id}/repost/`);
  post.reposted_by_me = data.reposted;
  post.reposts_count += data.reposted ? 1 : -1;
}

watch(() => route.params.handle, loadProfile);
onMounted(loadProfile);
</script>