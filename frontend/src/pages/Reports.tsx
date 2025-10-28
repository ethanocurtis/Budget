import { useEffect, useState } from 'react'
import { api } from '../lib/api'
export default function Reports(){
  const [data, setData] = useState<any>()
  useEffect(()=>{ api.get('/reports/spend-by-category').then(r=>setData(r.data)) },[])

  const exportCsv = ()=> window.location.href = (api.defaults.baseURL || '') + '/reports/export.csv'

  return (
    <div className="card">
      <h2 className="font-semibold mb-2">Reports</h2>
      <div>Income: ${data?.income?.toFixed?.(2) || '0.00'}</div>
      <div>Expense: ${Math.abs(data?.expense || 0).toFixed(2)}</div>
      <button className="btn mt-4" onClick={exportCsv}>Export CSV</button>
    </div>
  )
}
