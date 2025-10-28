/// <reference types="vite/client" />

// (Optional but explicit) declare the vars you use
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
