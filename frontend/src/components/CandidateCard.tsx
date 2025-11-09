import React from 'react';
import { Profile } from '../api/client';

type Props = {
  profile: Profile;
  onAccept: (id: number) => void;
  onReject: (id: number) => void;
};

export default function CandidateCard({ profile, onAccept, onReject }: Props) {
  return (
    <div className="card">
      <div className="card-media">
        {profile.photo_url ? (
          <img src={profile.photo_url} alt={profile.display_name} onError={(e) => {
            (e.currentTarget as HTMLImageElement).style.display = 'none';
          }} />
        ) : (
          <div className="placeholder">No Photo</div>
        )}
      </div>
      <div className="card-body">
        <div className="card-title">
          {profile.display_name}
          <span className="muted"> • {profile.gender}</span>
        </div>
        <div className="card-subtitle">
          {profile.height_cm ? `${profile.height_cm} cm` : '—'} · {profile.weight_kg ? `${profile.weight_kg} kg` : '—'}
        </div>
        {profile.bio && <p className="card-text">{profile.bio}</p>}
        <div className="card-actions">
          <button className="btn btn-outline error" onClick={() => onReject(profile.id)}>Reject</button>
          <button className="btn primary" onClick={() => onAccept(profile.id)}>Accept</button>
        </div>
      </div>
    </div>
  );
}
