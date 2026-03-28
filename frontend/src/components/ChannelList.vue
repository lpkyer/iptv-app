<template>
  <div class="flex flex-col h-full">
    <!-- Search -->
    <div class="px-3 py-2 border-b border-dark-600">
      <input
        v-model="store.searchQuery"
        type="text"
        placeholder="Rechercher une chaîne..."
        class="w-full bg-dark-700 border border-dark-500 text-white rounded-lg px-3 py-2 text-sm
               focus:outline-none focus:border-accent-500 placeholder:text-gray-600"
      />
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex-1 flex items-center justify-center">
      <div class="animate-spin rounded-full h-6 w-6 border-2 border-accent-500 border-t-transparent"></div>
    </div>

    <!-- Channels -->
    <div v-else class="flex-1 overflow-y-auto">
      <div
        v-for="stream in store.filteredStreams"
        :key="stream.stream_id"
        class="channel-card flex items-center gap-3 px-3 py-2.5 cursor-pointer border-l-2 border-transparent"
        :class="{ active: store.currentStream?.stream_id === stream.stream_id }"
        @click="$emit('select', stream)"
      >
        <!-- Logo -->
        <div class="w-8 h-8 rounded shrink-0 bg-dark-600 flex items-center justify-center overflow-hidden">
          <img
            v-if="stream.stream_icon"
            :src="stream.stream_icon"
            class="w-full h-full object-contain"
            @error="e => e.target.style.display='none'"
          />
          <span v-else class="text-xs text-gray-500">📺</span>
        </div>
        <!-- Name -->
        <span class="text-sm text-gray-300 truncate flex-1">{{ stream.name }}</span>
      </div>

      <div v-if="store.filteredStreams.length === 0 && !store.loading" class="text-center text-gray-600 text-sm py-8">
        Aucune chaîne trouvée
      </div>
    </div>
  </div>
</template>

<script setup>
import { useIptvStore } from '../stores/iptv'
const store = useIptvStore()
defineEmits(['select'])
</script>
