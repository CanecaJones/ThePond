<template>
  <div class="auth-page">
    <h1>🌊 The Pond</h1>
    <h2>Criar conta</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="handle" type="text" placeholder="@handle" required />
      <input v-model="password" type="password" placeholder="Senha" required />
      <button type="submit">Criar conta</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <router-link to="/login">Já tem conta? Entrar</router-link>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const username = ref("");
const handle = ref("");
const password = ref("");
const error = ref("");

const auth = useAuthStore();
const router = useRouter();

async function handleRegister() {
  error.value = "";
  try {
    await auth.register(username.value, handle.value, password.value);
    await auth.login(username.value, password.value);
    router.push("/");
  } catch (err) {
    error.value = "Erro ao criar conta. Verifique os dados.";
  }
}
</script>