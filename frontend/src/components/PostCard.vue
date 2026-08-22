<template>
  <article class="border-b border-pond-border px-4 py-3 hover:bg-pond-hover/50 transition-colors">
    <div class="flex gap-3">
      <div class="w-10 h-10 rounded-full bg-pond-surface flex items-center justify-center shrink-0 text-pond-muted">
        <User :size="20" />
      </div>

      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-1 text-[15px]">
          <span class="font-bold text-pond-text truncate">@{{ post.author.handle }}</span>
          <span class="text-pond-muted">- {{ timeAgo }}</span>
        </div>

        <p v-if="post.content" class="mt-1 whitespace-pre-wrap break-words">{{ post.content }}</p>

        <img
          v-if="post.image"
          :src="post.image"
          class="mt-3 rounded-2xl border border-pond-border max-h-[500px] w-full object-cover"
        />

        <div v-if="post.video" class="mt-3 relative rounded-2xl overflow-hidden border border-pond-border">
          <span class="absolute top-2 left-2 z-10 bg-pond-red text-white text-xs font-bold px-2 py-0.5 rounded-md flex items-center gap-1">
            <Play :size="12" fill="white" />
            <span>Video</span>
          </span>
          <video :src="post.video" controls class="w-full max-h-[500px] bg-black"></video>
        </div>

        <div v-if="post.audio" class="mt-3 flex items-center gap-2 bg-pond-surface border border-pond-border rounded-full px-3 py-2">
          <Music :size="16" class="text-pond-blue shrink-0" />
          <audio :src="post.audio" controls class="w-full h-8"></audio>
        </div>

        
        <a
            v-if="post.link"
            :href="post.link"
            target="_blank"
            rel="noopener"
            class="mt-3 flex items-center gap-2 border border-pond-border rounded-2xl px-3 py-2 text-pond-blue hover:bg-pond-surface truncate"
            >
            <Link2 :size="16" class="shrink-0" />
            <span class="truncate">{{ post.link }}</span>
        </a>

        <div class="flex items-center gap-8 mt-3 text-pond-muted text-sm">
          <button
            @click="handleLike"
            class="flex items-center gap-1.5 hover:text-pond-blue transition-colors"
          >
            <Heart
              :size="18"
              :fill="post.liked_by_me ? 'currentColor' : 'none'"
              :class="[post.liked_by_me ? 'text-pond-blue' : '', { 'animate-ripple rounded-full': rippling }]"
              @animationend="rippling = false"
            />
            <span>{{ post.likes_count }}</span>
          </button>

          <button
            @click="$emit('repost', post)"
            class="flex items-center gap-1.5 hover:text-pond-blue transition-colors"
            :class="{ 'text-pond-blue': post.reposted_by_me }"
          >
            <Repeat2 :size="18" />
            <span>{{ post.reposts_count }}</span>
          </button>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";
import { User, Music, Link2, Heart, Repeat2, Play } from "lucide-vue-next";

const props = defineProps({
  post: { type: Object, required: true },
});
const emit = defineEmits(["like", "repost"]);

const rippling = ref(false);

function handleLike() {
  rippling.value = true;
  emit("like", props.post);
}

const timeAgo = computed(() => {
  const diff = (Date.now() - new Date(props.post.created_at)) / 1000;
  if (diff < 60) return "agora";
  if (diff < 3600) return Math.floor(diff / 60) + "min";
  if (diff < 86400) return Math.floor(diff / 3600) + "h";
  return Math.floor(diff / 86400) + "d";
});
</script>