import { useEffect, useState } from 'react'
import { api } from '../lib/api'
export default function Dashboard(){
  const [me, setMe] = useState<any>()
  const [report, setReport] = useState<any>()

  useEffect(()=>{
    api.get('/users/me').then(r=>setMe(r.data)).catch(()=>{})
    api.get('/reports/spend-by-category').then(r=>setReport(r.data)).catch(()=>{})
  },[])

  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="card">
        <h2 className="font-semibold mb-2">Welcome</h2>
        <div>{me ? `Signed in as ${me.email}` : 'Not signed in — go to Settings > Login'}</div>
      </div>
      <div className="card">
        <h2 className="font-semibold mb-2">This Month</h2>
        <div>Income: ${report?.income?.toFixed?.(2) || '0.00'}</div>
        <div>Expense: ${Math.abs(report?.expense || 0).toFixed(2)}</div>
      </div>
    </div>
  )
}
