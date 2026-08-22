<template>
  <div class="min-h-screen flex items-center justify-center bg-pond-black px-4">
    <div class="w-full max-w-[380px] flex flex-col items-center">
      <AppLogo :size="64" />
      <h1 class="text-2xl font-bold mt-4">The Pond</h1>
      <h2 class="text-pond-muted mt-1 mb-6">Entrar na sua conta</h2>

      <form @submit.prevent="handleLogin" class="w-full flex flex-col gap-3">
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          required
          class="w-full bg-pond-black border border-pond-border rounded-md px-3 py-3 focus:outline-none focus:border-pond-blue"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Senha"
          required
          class="w-full bg-pond-black border border-pond-border rounded-md px-3 py-3 focus:outline-none focus:border-pond-blue"
        />
        <button
          type="submit"
          class="w-full bg-pond-red hover:bg-red-600 transition-colors text-white font-bold py-3 rounded-full mt-2"
        >
          Entrar
        </button>
      </form>

      <p v-if="error" class="text-pond-red text-sm mt-3">{{ error }}</p>

      <router-link to="/register" class="text-pond-blue text-sm mt-6 hover:underline">
        Não tem conta? Criar agora
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import AppLogo from "../components/AppLogo.vue";

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