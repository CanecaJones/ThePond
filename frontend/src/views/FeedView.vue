<template>
  <div class="feed-page">
    <header>
      <h1>The Pond</h1>
      <button @click="handleLogout">Sair</button>
    </header>

    <form class="new-post" @submit.prevent="handleCreatePost">
      <textarea v-model="content" maxlength="300" placeholder="O que está rolando?"></textarea>
      <small>{{ content.length }}/300</small>

      <div class="attachments">
        <label>
          Imagem
          <input type="file" accept="image/*" @change="onFileChange($event, 'image')" hidden />
        </label>
        <label>
          Vídeo (máx. 20MB)
          <input type="file" accept="video/*" @change="onFileChange($event, 'video')" hidden />
        </label>
        <label>
          Áudio
          <input type="file" accept="audio/*" @change="onFileChange($event, 'audio')" hidden />
        </label>
        <input v-model="link" type="url" placeholder="Link (opcional)" />
      </div>

      <p v-if="filePreviewName" class="file-preview">📎 {{ filePreviewName }}</p>
      <p v-if="formError" class="error">{{ formError }}</p>

      <button type="submit">Postar</button>
    </form>

    <div v-if="loading">Carregando feed...</div>
    <div v-else class="post-list">
      <div v-for="post in posts" :key="post.id" class="post">
        <strong>@{{ post.author.handle }}</strong>
        <p>{{ post.content }}</p>

        <img v-if="post.image" :src="post.image" class="post-media" alt="" />
        <video v-if="post.video" :src="post.video" controls class="post-media"></video>
        <audio v-if="post.audio" :src="post.audio" controls class="post-audio"></audio>
        <a v-if="post.link" :href="post.link" target="_blank" rel="noopener">{{ post.link }}</a>

        <div class="post-actions">
          <button @click="toggleLike(post)">
            {{ post.liked_by_me ? "💙" : "🤍" }} {{ post.likes_count }}
          </button>
          <button @click="toggleRepost(post)">
            {{ post.reposted_by_me ? "🔁" : "↻" }} {{ post.reposts_count }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import api from "../services/api";

const MAX_VIDEO_SIZE = 20 * 1024 * 1024; // 20MB

const posts = ref([]);
const content = ref("");
const link = ref("");
const loading = ref(true);
const formError = ref("");

const selectedFile = ref(null);
const selectedFileType = ref(null); // 'image' | 'video' | 'audio'
const filePreviewName = ref("");

const auth = useAuthStore();
const router = useRouter();

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