import { useEffect, useState } from 'react'
import { api } from '../lib/api'
export default function Transactions(){
  const [items, setItems] = useState<any[]>([])
  useEffect(()=>{
    api.get('/transactions').then(r=>setItems(r.data))
  },[])
  return (
    <div className="card">
      <h2 className="font-semibold mb-2">Transactions</h2>
      <table className="w-full text-sm">
        <thead><tr><th className="text-left">Date</th><th className="text-left">Payee</th><th className="text-left">Memo</th><th className="text-right">Amount</th></tr></thead>
        <tbody>
          {items.map(t=>(
            <tr key={t.id}>
              <td>{t.date}</td><td>{t.payee}</td><td>{t.memo}</td><td className="text-right">{Number(t.amount).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
