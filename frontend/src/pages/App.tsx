import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import Login from './Login'
import Dashboard from './Dashboard'
import Accounts from './Accounts'
import Transactions from './Transactions'
import Budgets from './Budgets'
import Reports from './Reports'
import Settings from './Settings'

export default function App(){
  return (
    <div>
      <nav className="border-b border-zinc-200 dark:border-zinc-800">
        <div className="container flex items-center gap-4 py-3">
          <Link to="/" className="font-semibold">Budgeteer</Link>
          <Link to="/accounts">Accounts</Link>
          <Link to="/transactions">Transactions</Link>
          <Link to="/budgets">Budgets</Link>
          <Link to="/reports">Reports</Link>
          <Link to="/settings" className="ml-auto">Settings</Link>
        </div>
      </nav>
      <div className="container py-6">
        <Routes>
          <Route path="/" element={<Dashboard/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/accounts" element={<Accounts/>} />
          <Route path="/transactions" element={<Transactions/>} />
          <Route path="/budgets" element={<Budgets/>} />
          <Route path="/reports" element={<Reports/>} />
          <Route path="/settings" element={<Settings/>} />
        </Routes>
      </div>
    </div>
  )
}
