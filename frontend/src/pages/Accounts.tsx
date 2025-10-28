import { useEffect, useState } from 'react'
import { api } from '../lib/api'
export default function Accounts(){
  const [items, setItems] = useState<any[]>([])
  const [name, setName] = useState('Checking')
  const [type, setType] = useState('checking')

  const load = ()=> api.get('/accounts').then(r=>setItems(r.data))
  useEffect(()=>{ load() },[])

  const add = async ()=>{
    await api.post('/accounts', {name, type, currency:'USD', opening_balance:0})
    load()
  }

  return (
    <div className="card">
      <h2 className="font-semibold mb-2">Accounts</h2>
      <div className="flex gap-2 mb-4">
        <input className="input" value={name} onChange={e=>setName(e.target.value)} />
        <select className="input" value={type} onChange={e=>setType(e.target.value)}>
          <option value="checking">checking</option><option value="savings">savings</option><option value="credit">credit</option><option value="cash">cash</option>
        </select>
        <button className="btn" onClick={add}>Add</button>
      </div>
      <ul className="space-y-2">{items.map(a=>(<li key={a.id} className="border-b border-zinc-700/10 pb-2">{a.name} <span className="text-xs text-zinc-500">({a.type})</span></li>))}</ul>
    </div>
  )
}
