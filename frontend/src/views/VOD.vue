<template>
  <div class="flex h-full overflow-hidden">
    <!-- Sidebar catégories -->
    <div class="w-48 shrink-0">
      <CategorySidebar
        :categories="store.categories"
        :selected="store.selectedCategory"
        @select="onCategorySelect"
      />
    </div>

    <!-- Grille VOD -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Search bar -->
      <div class="px-4 py-3 border-b border-dark-600 bg-dark-800">
        <input
          v-model="store.searchQuery"
          type="text"
          placeholder="Rechercher un film..."
          class="w-full max-w-sm bg-dark-700 border border-dark-500 text-white rounded-lg px-3 py-2 text-sm
                 focus:outline-none focus:border-accent-500 placeholder:text-gray-600"
        />
      </div>

      <!-- Loading -->
      <div v-if="store.loading" class="flex-1 flex items-center justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-2 border-accent-500 border-t-transparent"></div>
      </div>

      <!-- Grid -->
      <div v-else class="flex-1 overflow-y-auto p-4">
        <div v-if="activeStream" class="mb-4">
          <VideoPlayer :stream="activeStream" />
        </div>

        <div class="grid grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3">
          <div
            v-for="movie in store.filteredStreams"
            :key="movie.stream_id"
            class="bg-dark-800 rounded-lg overflow-hidden cursor-pointer hover:ring-2 hover:ring-accent-500 transition-all"
            :class="{ 'ring-2 ring-accent-500': activeStream?.stream_id === movie.stream_id }"
            @click="playVod(movie)"
          >
            <div class="aspect-[2/3] bg-dark-700 relative overflow-hidden">
              <img
                v-if="movie.stream_icon"
                :src="movie.stream_icon"
                class="w-full h-full object-cover"
                @error="e => e.target.style.display='none'"
              />
              <div v-else class="absolute inset-0 flex items-center justify-center text-4xl">🎬</div>
            </div>
            <div class="p-2">
              <p class="text-xs text-gray-300 font-medium line-clamp-2">{{ movie.name }}</p>
              <p v-if="movie.rating" class="text-xs text-yellow-400 mt-1">★ {{ movie.rating }}</p>
            </div>
          </div>
        </div>

        <div v-if="store.filteredStreams.length === 0" class="text-center text-gray-600 py-16">
          Aucun film trouvé
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useIptvStore } from '../stores/iptv'
import CategorySidebar from '../components/CategorySidebar.vue'
import VideoPlayer from '../components/VideoPlayer.vue'

const store = useIptvStore()
const activeStream = ref(null)

onMounted(async () => {
  await store.loadCategories('vod')
  await store.loadStreams('vod')
})

async function onCategorySelect(categoryId) {
  await store.loadStreams('vod', categoryId)
}

function playVod(movie) {
  store.selectStream(movie, 'vod')
  activeStream.value = store.currentStream
}
</script>
