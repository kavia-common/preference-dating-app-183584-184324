import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Auth } from '../lib/api'

export default function Login({ onAuthed }){
  const [email, setEmail] = useState('demo@example.com')
  const [username, setUsername] = useState('demo')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const nav = useNavigate()

  const submit = async (e)=>{
    e.preventDefault()
    setLoading(true); setError(null)
    try{
      const resp = await Auth.login(email, username)
      onAuthed(resp)
      nav('/')
    }catch(err){
      setError(String(err))
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{maxWidth:420, margin:'40px auto'}}>
      <h2 style={{marginTop:0}}>Welcome</h2>
      <p>Mock login to preview features.</p>
      <form onSubmit={submit} style={{display:'grid', gap:12}}>
        <input className="input" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email"/>
        <input className="input" value={username} onChange={e=>setUsername(e.target.value)} placeholder="Username"/>
        <button className="btn" disabled={loading}>{loading?'Signing in...':'Sign in'}</button>
        {error ? <div style={{color:'var(--error)'}}>{error}</div> : null}
      </form>
    </div>
  )
}
