import { useEffect, useState } from 'react'
import { api } from '../lib/api'
export default function Budgets(){
  const [month, setMonth] = useState(new Date().toISOString().slice(0,7))
  const [items, setItems] = useState<any[]>([])
  const [categoryId, setCategoryId] = useState<number>(0)
  const [planned, setPlanned] = useState('0')
  const [cats, setCats] = useState<any[]>([])

  const load = ()=> api.get('/budgets', { params:{month} }).then(r=>setItems(r.data))
  useEffect(()=>{ load(); api.get('/categories').then(r=>setCats(r.data)) },[month])

  const add = async ()=>{
    if(!categoryId) return
    await api.post('/budgets', {category_id: categoryId, month, planned: Number(planned)})
    setPlanned('0'); load()
  }

  return (
    <div className="card">
      <h2 className="font-semibold mb-2">Budgets</h2>
      <div className="flex gap-2 mb-4">
        <input className="input" type="month" value={month} onChange={e=>setMonth(e.target.value)} />
        <select className="input" onChange={e=>setCategoryId(Number(e.target.value))}>
          <option>Choose category...</option>
          {cats.map(c=>(<option key={c.id} value={c.id}>{c.name}</option>))}
        </select>
        <input className="input" type="number" value={planned} onChange={e=>setPlanned(e.target.value)} />
        <button className="btn" onClick={add}>Add</button>
      </div>
      <ul className="space-y-2">{items.map(b=>(<li key={b.id}>{b.month} — Category #{b.category_id}: ${Number(b.planned).toFixed(2)}</li>))}</ul>
    </div>
  )
}
