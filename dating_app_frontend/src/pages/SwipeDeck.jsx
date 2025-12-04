import React, { useEffect, useMemo, useState } from 'react'
import { Profiles, Swipes } from '../lib/api'

function useFilters(){
  // Very simple: read from a hidden storage (for demo; could connect via context or URL)
  const saved = localStorage.getItem('filters')
  const parsed = saved ? JSON.parse(saved) : {}
  return parsed
}

export default function SwipeDeck({ user }){
  const [cards, setCards] = useState([])
  const [idx, setIdx] = useState(0)

  const [filters, setFilters] = useState(()=>{
    const saved = localStorage.getItem('filters')
    return saved ? JSON.parse(saved) : { }
  })

  useEffect(()=>{
    const params = new URLSearchParams()
    if (filters.min_height_cm) params.set('min_height_cm', filters.min_height_cm)
    if (filters.max_height_cm) params.set('max_height_cm', filters.max_height_cm)
    if (filters.min_weight_kg) params.set('min_weight_kg', filters.min_weight_kg)
    if (filters.max_weight_kg) params.set('max_weight_kg', filters.max_weight_kg)
    if (filters.genders) params.set('genders', filters.genders)
    Profiles.discover(Object.fromEntries(params)).then((list)=>{
      setCards(list)
      setIdx(0)
    }).catch(()=>{})
  },[filters])

  useEffect(()=>{
    const handler = ()=>{
      const el = document.querySelector('input[type="hidden"][value^="{\\"min_height_cm"]')
      // Not robust; simplified demo to sync FiltersPanel choices by reading sibling input is omitted.
      // As a simple mechanism, use localStorage set by below.
    }
    window.addEventListener('filters-updated', handler)
    return ()=>window.removeEventListener('filters-updated', handler)
  },[])

  const current = cards[idx]

  const swipe = async (dir)=>{
    if (!user || !current) { setIdx(i=>i+1); return }
    try{
      await Swipes.swipe({ swiper_user_id: user.user_id, target_user_id: current.user_id, direction: dir })
    }catch{}
    setIdx(i=>i+1)
  }

  return (
    <div className="card">
      <h3 style={{marginTop:0}}>Discover</h3>
      {current ? (
        <>
          <div className="swipe-card" style={{backgroundImage:`url(${current.photo_url})`}}>
            <div className="overlay"></div>
            <div className="meta">
              <div style={{fontWeight:700, fontSize:20}}>{current.display_name}</div>
              <div style={{opacity:.9, fontSize:14}}>{current.height_cm? `${current.height_cm} cm` : ''} {current.weight_kg? `• ${current.weight_kg} kg` : ''}</div>
              <div style={{marginTop:6, opacity:.9}}>{current.bio}</div>
              <div style={{marginTop:8, display:'flex', gap:6, flexWrap:'wrap'}}>
                {current.interests?.map((t,i)=>(<span key={i} className="badge">{t}</span>))}
              </div>
            </div>
          </div>
          <div className="actions">
            <button className="action pass" onClick={()=>swipe('left')}>✖</button>
            <button className="action like" onClick={()=>swipe('right')}>♥</button>
          </div>
        </>
      ) : <div>No more profiles.</div>}
    </div>
  )
}
