<template>
  <div
    class="flex items-center justify-center rounded-full bg-pond-surface ring-2 ring-pond-blue/40"
    :style="{ width: size + 'px', height: size + 'px' }"
  >
    <!-- PLACEHOLDER: troque este SVG por <img src="/frog-logo.png" class="w-full h-full rounded-full object-cover" /> quando tiver a arte final do sapinho -->
    <svg
      :width="size * 0.6"
      :height="size * 0.6"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="1.6"
      class="text-pond-blue"
    >
      <ellipse cx="12" cy="15" rx="7" ry="5.5" />
      <circle cx="7" cy="7" r="2.4" />
      <circle cx="17" cy="7" r="2.4" />
      <circle cx="7" cy="7" r="0.6" fill="currentColor" />
      <circle cx="17" cy="7" r="0.6" fill="currentColor" />
      <path d="M9 16c1 1 5 1 6 0" />
    </svg>
  </div>
</template>

<script setup>
defineProps({
  size: { type: Number, default: 40 },
});
</script>