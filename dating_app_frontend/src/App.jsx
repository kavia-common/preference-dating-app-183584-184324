import React, { useEffect, useState } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import Login from './pages/Login'
import Profile from './pages/Profile'
import SwipeDeck from './pages/SwipeDeck'
import FiltersPanel from './pages/FiltersPanel'
import Chats from './pages/Chats'
import { Filters } from './lib/api'

export default function App(){
  const [user, setUser] = useState(null)
  const [filterOpen, setFilterOpen] = useState(false)
  const navigate = useNavigate()

  useEffect(()=>{
    const saved = localStorage.getItem('user')
    if (saved) setUser(JSON.parse(saved))
  },[])

  const handleLogout = ()=>{
    localStorage.removeItem('user')
    setUser(null)
    navigate('/login')
  }

  return (
    <div>
      <div className="topbar">
        <div className="nav container">
          <div style={{display:'flex', alignItems:'center', gap:8}}>
            <span style={{fontWeight:700, color:'var(--primary)'}}>Preference</span>
            <span className="badge">Ocean Professional</span>
          </div>
          <div style={{display:'flex', gap:8}}>
            <button className="btn secondary" onClick={()=>setFilterOpen(v=>!v)}>Filters</button>
            {user ? <button className="btn" onClick={handleLogout}>Logout</button> : null}
          </div>
        </div>
        {filterOpen ? <div className="container"><FiltersPanel /></div> : null}
      </div>

      <div className="container" style={{paddingBottom:80}}>
        <Routes>
          <Route path="/" element={<SwipeDeck user={user} />} />
          <Route path="/login" element={<Login onAuthed={(u)=>{ setUser(u); localStorage.setItem('user', JSON.stringify(u)); }}/>} />
          <Route path="/profile" element={<Profile user={user} />} />
          <Route path="/chats" element={<Chats user={user} />} />
        </Routes>
      </div>

      <div className="tabbar">
        <Link to="/" className="btn" style={{textDecoration:'none'}}>Discover</Link>
        <Link to="/chats" className="btn secondary" style={{textDecoration:'none'}}>Chats</Link>
        <Link to="/profile" className="btn" style={{textDecoration:'none'}}>Profile</Link>
      </div>
    </div>
  )
}
