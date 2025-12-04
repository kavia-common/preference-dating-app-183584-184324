import React, { useEffect, useState } from 'react'
import { Profiles } from '../lib/api'

export default function Profile({ user }){
  const [profile, setProfile] = useState(null)
  const [form, setForm] = useState({ display_name:'', bio:'', height_cm:'', weight_kg:'', photo_url:'', gender:'', interests:'' })
  const [msg, setMsg] = useState(null)

  useEffect(()=>{
    const run = async ()=>{
      if (!user) return
      try{
        const data = await Profiles.get(user.user_id)
        setProfile(data)
        setForm({
          display_name: data.display_name, bio: data.bio,
          height_cm: data.height_cm||'', weight_kg: data.weight_kg||'',
          photo_url: data.photo_url, gender: data.gender, interests: (data.interests||[]).join(', ')
        })
      }catch{
        setProfile(null)
      }
    }
    run()
  },[user])

  if (!user) return <div className="card">Please log in to edit your profile.</div>

  const save = async ()=>{
    try{
      if (!profile){
        const created = await Profiles.create({
          display_name: form.display_name,
          bio: form.bio,
          height_cm: Number(form.height_cm)||null,
          weight_kg: Number(form.weight_kg)||null,
          photo_url: form.photo_url,
          gender: form.gender,
          interests: form.interests.split(',').map(s=>s.trim()).filter(Boolean),
          user_id: user.user_id
        })
        setProfile(created)
      }else{
        const updated = await Profiles.update(user.user_id, {
          display_name: form.display_name,
          bio: form.bio,
          height_cm: Number(form.height_cm)||null,
          weight_kg: Number(form.weight_kg)||null,
          photo_url: form.photo_url,
          gender: form.gender,
          interests: form.interests.split(',').map(s=>s.trim()).filter(Boolean)
        })
        setProfile(updated)
      }
      setMsg('Saved!')
      setTimeout(()=>setMsg(null), 1500)
    }catch(e){
      setMsg(String(e))
    }
  }

  return (
    <div className="card">
      <h3 style={{marginTop:0}}>Your Profile</h3>
      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:12}}>
        <div>
          <label>Name</label>
          <input className="input" value={form.display_name} onChange={e=>setForm({...form, display_name:e.target.value})}/>
        </div>
        <div>
          <label>Photo URL</label>
          <input className="input" value={form.photo_url} onChange={e=>setForm({...form, photo_url:e.target.value})}/>
        </div>
        <div style={{gridColumn:'1/-1'}}>
          <label>Bio</label>
          <textarea className="input" value={form.bio} onChange={e=>setForm({...form, bio:e.target.value})}/>
        </div>
        <div>
          <label>Height (cm)</label>
          <input className="input" value={form.height_cm} onChange={e=>setForm({...form, height_cm:e.target.value})}/>
        </div>
        <div>
          <label>Weight (kg)</label>
          <input className="input" value={form.weight_kg} onChange={e=>setForm({...form, weight_kg:e.target.value})}/>
        </div>
        <div>
          <label>Gender</label>
          <input className="input" value={form.gender} onChange={e=>setForm({...form, gender:e.target.value})}/>
        </div>
        <div>
          <label>Interests (comma separated)</label>
          <input className="input" value={form.interests} onChange={e=>setForm({...form, interests:e.target.value})}/>
        </div>
      </div>
      <div style={{marginTop:12}}>
        <button className="btn" onClick={save}>Save</button>
        {msg ? <span style={{marginLeft:12}}>{msg}</span> : null}
      </div>
      {profile?.photo_url ? <div style={{marginTop:16}}><img src={profile.photo_url} alt="" style={{maxWidth:240, borderRadius:12}}/></div> : null}
    </div>
  )
}
