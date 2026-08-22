<template>
  <div class="min-h-screen bg-pond-black flex justify-center">
    <div class="flex w-full max-w-[990px]">
      <!-- Sidebar -->
      <aside class="w-[275px] shrink-0 hidden md:flex flex-col justify-between h-screen sticky top-0 px-3 py-4">
        <div>
          <AppLogo :size="44" />
          <nav class="mt-6 flex flex-col gap-1">
            <a class="flex items-center gap-4 px-3 py-3 rounded-full hover:bg-pond-surface font-bold cursor-pointer">
              <Home :size="24" /> <span class="text-base">Feed</span>
            </a>
            <a class="flex items-center gap-4 px-3 py-3 rounded-full hover:bg-pond-surface text-pond-muted cursor-not-allowed" title="Em breve">
              <Bell :size="24" /> <span class="text-base">Notificações</span>
            </a>
            <a class="flex items-center gap-4 px-3 py-3 rounded-full hover:bg-pond-surface text-pond-muted cursor-not-allowed" title="Em breve">
              <User :size="24" /> <span class="text-base">Perfil</span>
            </a>
          </nav>

          <button
            @click="focusCompose"
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

      <!-- Feed central -->
      <main class="w-full max-w-feed border-x border-pond-border min-h-screen">
        <header class="sticky top-0 bg-pond-black/80 backdrop-blur border-b border-pond-border px-4 py-3 z-10">
          <h1 class="text-xl font-bold">The Pond</h1>
        </header>

        <!-- Compose box -->
        <form @submit.prevent="handleCreatePost" class="border-b border-pond-border px-4 py-3">
          <div class="flex gap-3">
            <div class="w-10 h-10 rounded-full bg-pond-surface flex items-center justify-center shrink-0 text-pond-muted">
              <User :size="20" />
            </div>
            <div class="flex-1">
              <textarea
                ref="composeRef"
                v-model="content"
                maxlength="300"
                placeholder="O que está rolando na lagoa?"
                rows="2"
                class="w-full bg-transparent resize-none text-lg placeholder-pond-muted focus:outline-none"
              ></textarea>

              <input
                v-if="showLinkInput"
                v-model="link"
                type="url"
                placeholder="Cole o link aqui"
                class="w-full bg-pond-black border border-pond-border rounded-md px-3 py-2 mt-1 text-sm focus:outline-none focus:border-pond-blue"
              />

              <p v-if="filePreviewName" class="text-pond-blue text-sm mt-2">{{ filePreviewName }}</p>
              <p v-if="formError" class="text-pond-red text-sm mt-2">{{ formError }}</p>

              <div class="flex items-center justify-between mt-3 pt-3 border-t border-pond-border">
                <div class="flex items-center gap-1 text-pond-blue">
                  <label class="p-2 rounded-full hover:bg-pond-blue/10 cursor-pointer" title="Imagem">
                    <ImageIcon :size="20" />
                    <input type="file" accept="image/*" @change="onFileChange($event, 'image')" hidden />
                  </label>
                  <label class="p-2 rounded-full hover:bg-pond-blue/10 cursor-pointer" title="Vídeo (máx. 20MB)">
                    <VideoIcon :size="20" />
                    <input type="file" accept="video/*" @change="onFileChange($event, 'video')" hidden />
                  </label>
                  <label class="p-2 rounded-full hover:bg-pond-blue/10 cursor-pointer" title="Áudio">
                    <Music :size="20" />
                    <input type="file" accept="audio/*" @change="onFileChange($event, 'audio')" hidden />
                  </label>
                  <button
                    type="button"
                    @click="showLinkInput = !showLinkInput"
                    class="p-2 rounded-full hover:bg-pond-blue/10"
                    title="Link"
                  >
                    <Link2 :size="20" />
                  </button>
                </div>

                <div class="flex items-center gap-3">
                  <span class="text-xs text-pond-muted">{{ content.length }}/300</span>
                  <button
                    type="submit"
                    class="bg-pond-red hover:bg-red-600 transition-colors text-white font-bold px-5 py-1.5 rounded-full disabled:opacity-50"
                  >
                    Postar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </form>

        <!-- Lista de posts -->
        <div v-if="loading" class="text-center text-pond-muted py-10">Carregando o feed...</div>
        <div v-else>
          <PostCard
            v-for="post in posts"
            :key="post.id"
            :post="post"
            @like="toggleLike"
            @repost="toggleRepost"
          />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import api from "../services/api";
import AppLogo from "../components/AppLogo.vue";
import PostCard from "../components/PostCard.vue";
import {
  Home, Bell, User, Image as ImageIcon, Video as VideoIcon,
  Music, Link2, LogOut,
} from "lucide-vue-next";

const MAX_VIDEO_SIZE = 20 * 1024 * 1024;

const posts = ref([]);
const content = ref("");
const link = ref("");
const showLinkInput = ref(false);
const loading = ref(true);
const formError = ref("");
const composeRef = ref(null);

const selectedFile = ref(null);
const selectedFileType = ref(null);
const filePreviewName = ref("");

const auth = useAuthStore();
const router = useRouter();

function focusCompose() {
  composeRef.value?.focus();
}

function onFileChange(event, type) {
  const file = event.target.files[0];
  if (!file) return;

  if (type === "video" && file.size > MAX_VIDEO_SIZE) {
    formError.value = "O vídeo não pode passar de 20MB.";
    event.target.value = "";
    return;
  }

  formError.value = "";
  selectedFile.value = file;
  selectedFileType.value = type;
  filePreviewName.value = file.name;
}

async function loadFeed() {
  loading.value = true;
  const { data } = await api.get("/posts/");
  posts.value = data;
  loading.value = false;
}

async function handleCreatePost() {
  if (!content.value.trim() && !selectedFile.value && !link.value.trim()) {
    formError.value = "O post precisa ter texto, mídia ou link.";
    return;
  }

  const formData = new FormData();
  formData.append("content", content.value);
  if (link.value.trim()) formData.append("link", link.value.trim());
  if (selectedFile.value) {
    formData.append(selectedFileType.value, selectedFile.value);
  }

  try {
    await api.post("/posts/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    content.value = "";
    link.value = "";
    showLinkInput.value = false;
    selectedFile.value = null;
    selectedFileType.value = null;
    filePreviewName.value = "";
    formError.value = "";
    await loadFeed();
  } catch (err) {
    formError.value = "Erro ao criar post.";
  }
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

function handleLogout() {
  auth.logout();
  router.push("/login");
}

onMounted(loadFeed);
</script>