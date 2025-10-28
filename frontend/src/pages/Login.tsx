import { useState } from 'react'
import { api } from '../lib/api'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const [email, setEmail] = useState('demo@demo.com')
  const [password, setPassword] = useState('demo123')
  const [err, setErr] = useState<string|undefined>()
  const nav = useNavigate()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    try{
      const r = await api.post('/auth/login', {email, password})
      localStorage.setItem('access_token', r.data.access_token)
      localStorage.setItem('refresh_token', r.data.refresh_token)
      nav('/')
    }catch(e:any){
      setErr(e?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="max-w-sm mx-auto card">
      <h1 className="text-xl mb-4 font-semibold">Login</h1>
      {err && <div className="mb-3 text-red-600">{err}</div>}
      <form onSubmit={submit} className="space-y-3">
        <input className="input w-full" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email"/>
        <input className="input w-full" type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password"/>
        <button className="btn w-full">Sign in</button>
      </form>
    </div>
  )
}
