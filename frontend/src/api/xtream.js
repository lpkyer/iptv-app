import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

function getCreds() {
  const raw = localStorage.getItem('iptv_creds')
  if (!raw) throw new Error('Non authentifié')
  return JSON.parse(raw)
}

export async function authenticate(host, username, password) {
  const { data } = await api.post('/auth', { host, username, password })
  return data
}

export async function getLiveCategories() {
  const creds = getCreds()
  const { data } = await api.get('/live/categories', { params: creds })
  return data
}

export async function getLiveStreams(category_id = null) {
  const creds = getCreds()
  const params = { ...creds }
  if (category_id) params.category_id = category_id
  const { data } = await api.get('/live/streams', { params })
  return data
}

export async function getVodCategories() {
  const creds = getCreds()
  const { data } = await api.get('/vod/categories', { params: creds })
  return data
}

export async function getVodStreams(category_id = null) {
  const creds = getCreds()
  const params = { ...creds }
  if (category_id) params.category_id = category_id
  const { data } = await api.get('/vod/streams', { params })
  return data
}

export function buildStreamUrl(streamId, ext = 'm3u8') {
  const { host, username, password } = getCreds()
  const streamUrl = `${host}/live/${username}/${password}/${streamId}.${ext}`
  // On passe par le proxy pour éviter les problèmes CORS
  return `/api/stream/proxy?url=${encodeURIComponent(streamUrl)}`
}

export function buildVodUrl(streamId, ext = 'mp4') {
  const { host, username, password } = getCreds()
  const vodUrl = `${host}/movie/${username}/${password}/${streamId}.${ext}`
  return `/api/stream/proxy?url=${encodeURIComponent(vodUrl)}`
}
