import React, { useEffect, useState } from 'react'
import { Filters } from '../lib/api'

export default function FiltersPanel(){
  const [minH, setMinH] = useState('')
  const [maxH, setMaxH] = useState('')
  const [minW, setMinW] = useState('')
  const [maxW, setMaxW] = useState('')
  const [genders, setGenders] = useState([])
  const [presets, setPresets] = useState([])

  useEffect(()=>{
    Filters.presets().then(setPresets).catch(()=>{})
  },[])

  const toggleG = (g)=>{
    setGenders(gs => gs.includes(g) ? gs.filter(x=>x!==g) : [...gs, g])
  }

  const applyPreset = (p)=>{
    setMinH(p.min_height_cm ?? '')
    setMaxH(p.max_height_cm ?? '')
    setMinW(p.min_weight_kg ?? '')
    setMaxW(p.max_weight_kg ?? '')
    setGenders(p.genders || [])
  }

  return (
    <div className="card" style={{margin:'12px 0'}}>
      <div style={{display:'flex', gap:8, flexWrap:'wrap', marginBottom:8}}>
        {presets.map((p,i)=>(
          <button key={i} className="btn secondary" onClick={()=>applyPreset(p)}>{p.name}</button>
        ))}
      </div>
      <div style={{display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap:8}}>
        <input className="input" placeholder="Min cm" value={minH} onChange={e=>setMinH(e.target.value)}/>
        <input className="input" placeholder="Max cm" value={maxH} onChange={e=>setMaxH(e.target.value)}/>
        <input className="input" placeholder="Min kg" value={minW} onChange={e=>setMinW(e.target.value)}/>
        <input className="input" placeholder="Max kg" value={maxW} onChange={e=>setMaxW(e.target.value)}/>
      </div>
      <div style={{marginTop:8, display:'flex', gap:8, flexWrap:'wrap'}}>
        {['male','female','nonbinary'].map(g=>(
          <span key={g} className="badge" onClick={()=>toggleG(g)} style={{cursor:'pointer', border: genders.includes(g)?'2px solid var(--primary)':'2px solid transparent'}}>{g}</span>
        ))}
      </div>
      <div style={{marginTop:8, color:'#6b7280', fontSize:12}}>
        Filters are applied in Discover when you refresh or navigate there.
      </div>
      <input type="hidden" value={JSON.stringify({min_height_cm:minH, max_height_cm:maxH, min_weight_kg:minW, max_weight_kg:maxW, genders:genders.join(',')})} readOnly/>
    </div>
  )
}
