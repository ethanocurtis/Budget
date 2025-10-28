import axios from 'axios'

// Auto-detect API on same host (swap :8080 -> :8000), unless Vite env overrides it.
const detected = (() => {
  const { protocol, hostname } = window.location
  // IPv6 safety (not strictly needed here, but harmless)
  const host = hostname.includes(':') ? `[${hostname}]` : hostname
  return `${protocol}//${host}:8000`
})()

const API_BASE_URL =
  (import.meta as any).env?.VITE_API_BASE_URL || detected

export const api = axios.create({
  baseURL: API_BASE_URL + '/api/v1'
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
