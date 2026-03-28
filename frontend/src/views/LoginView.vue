<template>
  <div class="min-h-screen flex items-center justify-center bg-dark-900">
    <div class="w-full max-w-md p-8 bg-dark-800 rounded-2xl border border-dark-600 shadow-2xl">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="text-5xl mb-3">📺</div>
        <h1 class="text-2xl font-bold text-white">IPTV Player</h1>
        <p class="text-gray-500 text-sm mt-1">Entrez vos credentials Xtream</p>
      </div>

      <!-- Form -->
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-gray-400 mb-1.5 uppercase tracking-wide">
            URL du serveur
          </label>
          <input
            v-model="form.host"
            type="text"
            placeholder="http://votre-serveur.com:8080"
            class="input-field"
          />
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-400 mb-1.5 uppercase tracking-wide">
            Nom d'utilisateur
          </label>
          <input
            v-model="form.username"
            type="text"
            placeholder="username"
            class="input-field"
          />
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-400 mb-1.5 uppercase tracking-wide">
            Mot de passe
          </label>
          <input
            v-model="form.password"
            type="password"
            placeholder="••••••••"
            class="input-field"
            @keyup.enter="login"
          />
        </div>

        <!-- Erreur -->
        <div v-if="error" class="text-red-400 text-sm bg-red-950 border border-red-800 rounded-lg p-3">
          {{ error }}
        </div>

        <!-- Submit -->
        <button
          @click="login"
          :disabled="loading"
          class="w-full py-3 bg-accent-500 hover:bg-accent-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-colors mt-2"
        >
          <span v-if="loading">Connexion en cours...</span>
          <span v-else>Se connecter</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authenticate } from '../api/xtream'

const router = useRouter()
const loading = ref(false)
const error = ref(null)

const form = reactive({
  host: '',
  username: '',
  password: ''
})

async function login() {
  if (!form.host || !form.username || !form.password) {
    error.value = 'Tous les champs sont requis'
    return
  }
  loading.value = true
  error.value = null
  try {
    await authenticate(form.host, form.username, form.password)
    localStorage.setItem('iptv_creds', JSON.stringify({
      host: form.host,
      username: form.username,
      password: form.password
    }))
    router.push('/live')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Connexion impossible. Vérifiez vos credentials.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input-field {
  @apply w-full bg-dark-700 border border-dark-500 text-white rounded-xl px-4 py-3 text-sm
         focus:outline-none focus:border-accent-500 focus:ring-1 focus:ring-accent-500
         placeholder:text-gray-600 transition-colors;
}
</style>
