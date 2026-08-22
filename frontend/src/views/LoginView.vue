<template>
  <div class="auth-page">
    <h1>🌊 The Pond</h1>
    <h2>Entrar</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Senha" required />
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <router-link to="/register">Criar conta</router-link>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const username = ref("");
const password = ref("");
const error = ref("");

const auth = useAuthStore();
const router = useRouter();

async function handleLogin() {
  error.value = "";
  try {
    await auth.login(username.value, password.value);
    router.push("/");
  } catch (err) {
    error.value = "Usuário ou senha inválidos.";
  }
}
</script>