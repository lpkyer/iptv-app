import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as api from '../api/xtream'

export const useIptvStore = defineStore('iptv', () => {
  // ── State ──────────────────────────────────────────────────────────────────
  const categories = ref([])
  const streams = ref([])
  const currentStream = ref(null)
  const selectedCategory = ref(null)
  const searchQuery = ref('')
  const loading = ref(false)
  const error = ref(null)

  // ── Getters ────────────────────────────────────────────────────────────────
  const filteredStreams = computed(() => {
    if (!searchQuery.value) return streams.value
    const q = searchQuery.value.toLowerCase()
    return streams.value.filter(s =>
      s.name.toLowerCase().includes(q)
    )
  })

  // ── Actions ────────────────────────────────────────────────────────────────
  async function loadCategories(type = 'live') {
    loading.value = true
    error.value = null
    try {
      categories.value = type === 'live'
        ? await api.getLiveCategories()
        : await api.getVodCategories()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function loadStreams(type = 'live', categoryId = null) {
    loading.value = true
    error.value = null
    selectedCategory.value = categoryId
    try {
      streams.value = type === 'live'
        ? await api.getLiveStreams(categoryId)
        : await api.getVodStreams(categoryId)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  function selectStream(stream, type = 'live') {
    const ext = type === 'live' ? 'm3u8' : 'mp4'
    const urlFn = type === 'live' ? api.buildStreamUrl : api.buildVodUrl
    currentStream.value = {
      ...stream,
      url: urlFn(stream.stream_id, ext),
      type,
    }
  }

  function reset() {
    categories.value = []
    streams.value = []
    currentStream.value = null
    selectedCategory.value = null
    searchQuery.value = ''
  }

  return {
    categories, streams, currentStream, selectedCategory,
    searchQuery, loading, error, filteredStreams,
    loadCategories, loadStreams, selectStream, reset
  }
})
