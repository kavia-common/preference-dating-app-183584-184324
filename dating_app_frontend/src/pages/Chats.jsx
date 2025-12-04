import React, { useEffect, useState } from 'react'
import { Matches, Messages } from '../lib/api'

export default function Chats({ user }){
  const [matches, setMatches] = useState([])
  const [active, setActive] = useState(null)
  const [messages, setMessages] = useState([])
  const [text, setText] = useState('')

  useEffect(()=>{
    if (!user) return
    Matches.list(user.user_id).then(setMatches).catch(()=>{})
  },[user])

  useEffect(()=>{
    if (!active) return
    const load = ()=> Messages.list(active.id).then(setMessages).catch(()=>{})
    load()
    const timer = setInterval(load, 2000) // short polling MVP
    return ()=>clearInterval(timer)
  },[active])

  if (!user) return <div className="card">Login to view chats.</div>

  const send = async ()=>{
    if (!text.trim()) return
    await Messages.send({ match_id: active.id, sender_id: user.user_id, content: text })
    setText('')
    const updated = await Messages.list(active.id)
    setMessages(updated)
  }

  return (
    <div className="card">
      <h3 style={{marginTop:0}}>Chats</h3>
      <div style={{display:'grid', gridTemplateColumns:'240px 1fr', gap:12}}>
        <div>
          <div style={{display:'grid', gap:8}}>
            {matches.map(m=>(
              <button key={m.id} className="btn secondary" onClick={()=>setActive(m)} style={{justifyContent:'flex-start'}}>
                Match #{m.id} • {m.user_a_id === user.user_id ? m.user_b_id : m.user_a_id}
              </button>
            ))}
          </div>
        </div>
        <div>
          {active ? (
            <>
              <div className="card" style={{height:300, overflow:'auto', background:'#f3f4f6'}}>
                {messages.map(msg=>(
                  <div key={msg.id} style={{display:'flex', justifyContent: msg.sender_id===user.user_id?'flex-end':'flex-start', margin:'6px 0'}}>
                    <div style={{background: msg.sender_id===user.user_id?'#DBEAFE':'white', padding:'8px 12px', borderRadius:12, maxWidth:'70%'}}>
                      {msg.content}
                    </div>
                  </div>
                ))}
              </div>
              <div style={{display:'flex', gap:8, marginTop:8}}>
                <input className="input" value={text} onChange={e=>setText(e.target.value)} placeholder="Type a message..."/>
                <button className="btn" onClick={send}>Send</button>
              </div>
            </>
          ) : <div>Select a conversation</div>}
        </div>
      </div>
    </div>
  )
}
