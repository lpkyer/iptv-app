<template>
  <div class="h-screen flex flex-col bg-dark-900">
    <!-- Navbar (cachée sur login) -->
    <nav v-if="isAuthenticated" class="flex items-center justify-between px-6 py-3 bg-dark-800 border-b border-dark-600 shrink-0">
      <div class="flex items-center gap-2">
        <span class="text-2xl">📺</span>
        <span class="font-bold text-white text-lg tracking-tight">IPTV Player</span>
      </div>
      <div class="flex items-center gap-1">
        <router-link to="/live" class="nav-link" :class="{ active: $route.path === '/live' }">
          Live TV
        </router-link>
        <router-link to="/vod" class="nav-link" :class="{ active: $route.path === '/vod' }">
          VOD
        </router-link>
      </div>
      <button @click="logout" class="text-sm text-gray-400 hover:text-white transition-colors px-3 py-1 rounded hover:bg-dark-600">
        Déconnexion
      </button>
    </nav>

    <!-- Vue principale -->
    <div class="flex-1 overflow-hidden">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isAuthenticated = computed(() => !!localStorage.getItem('iptv_creds'))

function logout() {
  localStorage.removeItem('iptv_creds')
  router.push('/login')
}
</script>

<style>
.nav-link {
  @apply px-4 py-2 rounded text-sm font-medium text-gray-400 hover:text-white transition-colors;
}
.nav-link.active {
  @apply text-white bg-dark-600;
}
</style>
