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

    <!-- Liste de chaînes -->
    <div class="w-72 shrink-0 border-r border-dark-600 bg-dark-800">
      <ChannelList @select="onStreamSelect" />
    </div>

    <!-- Lecteur + info -->
    <div class="flex-1 flex flex-col p-4 gap-4 overflow-auto">
      <VideoPlayer :stream="store.currentStream" />

      <!-- Info chaîne active -->
      <div v-if="store.currentStream" class="bg-dark-800 rounded-xl p-4 border border-dark-600">
        <div class="flex items-center gap-3">
          <img
            v-if="store.currentStream.stream_icon"
            :src="store.currentStream.stream_icon"
            class="w-10 h-10 rounded object-contain bg-dark-700 p-1"
            @error="e => e.target.style.display='none'"
          />
          <div>
            <h2 class="text-white font-semibold">{{ store.currentStream.name }}</h2>
            <p class="text-gray-500 text-xs mt-0.5">ID: {{ store.currentStream.stream_id }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useIptvStore } from '../stores/iptv'
import CategorySidebar from '../components/CategorySidebar.vue'
import ChannelList from '../components/ChannelList.vue'
import VideoPlayer from '../components/VideoPlayer.vue'

const store = useIptvStore()

onMounted(async () => {
  await store.loadCategories('live')
  await store.loadStreams('live')
})

async function onCategorySelect(categoryId) {
  await store.loadStreams('live', categoryId)
}

function onStreamSelect(stream) {
  store.selectStream(stream, 'live')
}
</script>
