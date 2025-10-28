import { Link } from 'react-router-dom'
export default function Settings(){
  return (
    <div className="card">
      <h2 className="font-semibold mb-2">Settings</h2>
      <p>Authentication: <Link to="/login" className="underline">Sign in</Link></p>
      <p>Data: Export/Import via API endpoints.</p>
    </div>
  )
}
