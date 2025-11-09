import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api, Profile, ProfileCreate, ProfileUpdate } from '../api/client';

type FormState = {
  user_id: number;
  display_name: string;
  bio: string;
  height_cm: string;
  weight_kg: string;
  gender: string;
  photo_url: string;
};

const emptyForm: FormState = {
  user_id: 1,
  display_name: '',
  bio: '',
  height_cm: '',
  weight_kg: '',
  gender: 'unspecified',
  photo_url: ''
};

export default function ProfileFormPage() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [form, setForm] = React.useState<FormState>(emptyForm);
  const [loading, setLoading] = React.useState<boolean>(!!isEdit);
  const [submitting, setSubmitting] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [success, setSuccess] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (!isEdit) return;
    setLoading(true);
    api.getProfile(Number(id))
      .then((p: Profile) => {
        setForm({
          user_id: p.user_id,
          display_name: p.display_name || '',
          bio: p.bio || '',
          height_cm: p.height_cm != null ? String(p.height_cm) : '',
          weight_kg: p.weight_kg != null ? String(p.weight_kg) : '',
          gender: p.gender || 'unspecified',
          photo_url: p.photo_url || ''
        });
      })
      .catch((e) => setError(e.message || String(e)))
      .finally(() => setLoading(false));
  }, [id, isEdit]);

  const onChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(null);
    try {
      if (isEdit) {
        const payload: ProfileUpdate = {
          display_name: form.display_name,
          bio: form.bio,
          height_cm: form.height_cm ? Number(form.height_cm) : null,
          weight_kg: form.weight_kg ? Number(form.weight_kg) : null,
          gender: form.gender,
          photo_url: form.photo_url
        };
        const updated = await api.updateProfile(Number(id), payload);
        setSuccess(`Updated profile #${updated.id}`);
      } else {
        const payload: ProfileCreate = {
          user_id: Number(form.user_id),
          display_name: form.display_name,
          bio: form.bio,
          height_cm: form.height_cm ? Number(form.height_cm) : null,
          weight_kg: form.weight_kg ? Number(form.weight_kg) : null,
          gender: form.gender,
          photo_url: form.photo_url,
          interests: []
        };
        const created = await api.createProfile(payload);
        setSuccess(`Created profile #${created.id}`);
        navigate(`/profile/${created.id}`, { replace: true });
      }
    } catch (e: any) {
      setError(e.message || String(e));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="panel">
      <div className="panel-title">{isEdit ? 'Edit Profile' : 'Create Profile'}</div>
      {loading && <div className="muted">Loading profile...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!loading && (
        <form className="form" onSubmit={onSubmit}>
          {!isEdit && (
            <label className="field">
              <span className="label">User ID</span>
              <input type="number" name="user_id" value={form.user_id} onChange={onChange} min={1} required />
            </label>
          )}
          <label className="field">
            <span className="label">Display Name</span>
            <input name="display_name" value={form.display_name} onChange={onChange} required />
          </label>
          <label className="field">
            <span className="label">Bio</span>
            <textarea name="bio" value={form.bio} onChange={onChange} rows={3} />
          </label>
          <div className="grid">
            <label className="field">
              <span className="label">Height (cm)</span>
              <input type="number" name="height_cm" value={form.height_cm} onChange={onChange} min={0} placeholder="e.g., 175" />
            </label>
            <label className="field">
              <span className="label">Weight (kg)</span>
              <input type="number" name="weight_kg" value={form.weight_kg} onChange={onChange} min={0} placeholder="e.g., 70" />
            </label>
          </div>
          <div className="grid">
            <label className="field">
              <span className="label">Gender</span>
              <select name="gender" value={form.gender} onChange={onChange}>
                <option value="unspecified">Unspecified</option>
                <option value="female">Female</option>
                <option value="male">Male</option>
                <option value="nonbinary">Non-binary</option>
                <option value="other">Other</option>
              </select>
            </label>
            <label className="field">
              <span className="label">Photo URL</span>
              <input name="photo_url" value={form.photo_url} onChange={onChange} placeholder="https://..." />
            </label>
          </div>
          <div className="row-between">
            <div>
              {success && <div className="success">{success}</div>}
              {error && <div className="error">Error: {error}</div>}
            </div>
            <button className="btn primary" type="submit" disabled={submitting}>
              {submitting ? 'Saving...' : (isEdit ? 'Save Changes' : 'Create Profile')}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
