<template>
  <div class="feed-page">
    <header>
      <h1>🌊 The Pond</h1>
      <button @click="handleLogout">Sair</button>
    </header>

    <form class="new-post" @submit.prevent="handleCreatePost">
      <textarea v-model="content" maxlength="300" placeholder="O que está rolando?"></textarea>
      <small>{{ content.length }}/300</small>
      <button type="submit">Postar</button>
    </form>

    <div v-if="loading">Carregando feed...</div>
    <div v-else class="post-list">
      <div v-for="post in posts" :key="post.id" class="post">
        <strong>@{{ post.author.handle }}</strong>
        <p>{{ post.content }}</p>
        <img v-if="post.image" :src="post.image" alt="" />
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

const posts = ref([]);
const content = ref("");
const loading = ref(true);

const auth = useAuthStore();
const router = useRouter();

async function loadFeed() {
  loading.value = true;
  const { data } = await api.get("/posts/");
  posts.value = data;
  loading.value = false;
}

async function handleCreatePost() {
  if (!content.value.trim()) return;
  await api.post("/posts/", { content: content.value });
  content.value = "";
  await loadFeed();
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