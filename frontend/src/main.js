import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

import LoginView from './views/LoginView.vue'
import LiveTV from './views/LiveTV.vue'
import VOD from './views/VOD.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginView },
    { path: '/live', component: LiveTV, meta: { requiresAuth: true } },
    { path: '/vod', component: VOD, meta: { requiresAuth: true } },
  ]
})

router.beforeEach((to, from, next) => {
  const creds = localStorage.getItem('iptv_creds')
  if (to.meta.requiresAuth && !creds) {
    next('/login')
  } else {
    next()
  }
})

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')
