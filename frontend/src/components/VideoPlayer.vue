<template>
  <div class="relative bg-black w-full aspect-video rounded-xl overflow-hidden">
    <!-- Placeholder -->
    <div v-if="!stream" class="absolute inset-0 flex flex-col items-center justify-center text-gray-600">
      <span class="text-5xl mb-3">📺</span>
      <p class="text-sm">Sélectionnez une chaîne</p>
    </div>

    <!-- Loading overlay -->
    <div v-if="stream && loading" class="absolute inset-0 flex items-center justify-center bg-black/60 z-10">
      <div class="animate-spin rounded-full h-10 w-10 border-2 border-accent-500 border-t-transparent"></div>
    </div>

    <!-- Error overlay -->
    <div v-if="streamError" class="absolute inset-0 flex flex-col items-center justify-center bg-black/80 z-10">
      <span class="text-3xl mb-2">⚠️</span>
      <p class="text-red-400 text-sm text-center px-4">{{ streamError }}</p>
      <button @click="retryLoad" class="mt-3 text-xs bg-dark-600 px-4 py-2 rounded-lg hover:bg-dark-500 transition-colors">
        Réessayer
      </button>
    </div>

    <!-- Video -->
    <video
      ref="videoEl"
      class="w-full h-full"
      controls
      playsinline
      @waiting="loading = true"
      @canplay="loading = false"
      @error="handleVideoError"
    />

    <!-- Stream info overlay -->
    <div v-if="stream && !loading" class="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/80 to-transparent pointer-events-none">
      <div class="flex items-center gap-2">
        <img
          v-if="stream.stream_icon"
          :src="stream.stream_icon"
          class="w-6 h-6 rounded object-contain"
          @error="e => e.target.style.display='none'"
        />
        <span class="text-white text-sm font-medium truncate">{{ stream.name }}</span>
        <span class="ml-auto text-xs text-green-400 bg-green-950 px-2 py-0.5 rounded-full">● LIVE</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import Hls from 'hls.js'

const props = defineProps({
  stream: { type: Object, default: null }
})

const videoEl = ref(null)
const loading = ref(false)
const streamError = ref(null)
let hls = null

function destroyHls() {
  if (hls) {
    hls.destroy()
    hls = null
  }
}

function loadStream(streamObj) {
  if (!streamObj || !videoEl.value) return
  destroyHls()
  streamError.value = null
  loading.value = true
  const url = streamObj.url

  if (Hls.isSupported()) {
    hls = new Hls({
      enableWorker: true,
      lowLatencyMode: true,
    })
    hls.loadSource(url)
    hls.attachMedia(videoEl.value)
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      videoEl.value.play().catch(() => {})
    })
    hls.on(Hls.Events.ERROR, (_, data) => {
      if (data.fatal) {
        streamError.value = `Erreur de lecture: ${data.type}`
        loading.value = false
      }
    })
  } else if (videoEl.value.canPlayType('application/vnd.apple.mpegurl')) {
    // Safari natif
    videoEl.value.src = url
    videoEl.value.play().catch(() => {})
  } else {
    streamError.value = 'HLS non supporté par ce navigateur'
    loading.value = false
  }
}

function handleVideoError() {
  streamError.value = 'Impossible de charger le stream. Le serveur est peut-être indisponible.'
  loading.value = false
}

function retryLoad() {
  if (props.stream) loadStream(props.stream)
}

watch(() => props.stream, (newStream) => {
  if (newStream) loadStream(newStream)
}, { immediate: true })

onUnmounted(destroyHls)
</script>
