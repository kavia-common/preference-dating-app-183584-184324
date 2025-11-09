const BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');

export type HeightCategory = {
  id: number;
  name: string;
  min_cm: number | null;
  max_cm: number | null;
};

export type WeightCategory = {
  id: number;
  name: string;
  min_kg: number | null;
  max_kg: number | null;
};

export type Profile = {
  id: number;
  user_id: number;
  display_name: string;
  bio?: string | null;
  height_cm?: number | null;
  weight_kg?: number | null;
  gender: string;
  photo_url?: string | null;
  interests?: any[];
};

export type ProfileCreate = Omit<Profile, 'id'>;
export type ProfileUpdate = Partial<Omit<Profile, 'id' | 'user_id'>>;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {})
    },
    ...init
  });
  if (!res.ok) {
    const contentType = res.headers.get('content-type') || '';
    let detail: any = undefined;
    if (contentType.includes('application/json')) {
      try {
        detail = await res.json();
      } catch {
        detail = await res.text();
      }
    } else {
      detail = await res.text();
    }
    throw new Error(`HTTP ${res.status} ${res.statusText}: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`);
  }
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    return res.json() as Promise<T>;
  }
  // @ts-expect-error allow unknown types
  return res.text() as T;
}

export const api = {
  // PUBLIC_INTERFACE
  async listProfiles(params?: { height_category_id?: number | null; weight_category_id?: number | null; }): Promise<Profile[]> {
    const qp = new URLSearchParams();
    if (params?.height_category_id != null) qp.set('height_category_id', String(params.height_category_id));
    if (params?.weight_category_id != null) qp.set('weight_category_id', String(params.weight_category_id));
    const qs = qp.toString();
    return request<Profile[]>(`/profiles${qs ? `?${qs}` : ''}`);
  },

  // PUBLIC_INTERFACE
  async createProfile(payload: ProfileCreate): Promise<Profile> {
    return request<Profile>('/profiles', { method: 'POST', body: JSON.stringify(payload) });
  },

  // PUBLIC_INTERFACE
  async updateProfile(id: number, payload: ProfileUpdate): Promise<Profile> {
    return request<Profile>(`/profiles/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
  },

  // PUBLIC_INTERFACE
  async getProfile(id: number): Promise<Profile> {
    return request<Profile>(`/profiles/${id}`);
  },

  // PUBLIC_INTERFACE
  async getHeightCategories(): Promise<HeightCategory[]> {
    return request<HeightCategory[]>('/categories/height');
  },

  // PUBLIC_INTERFACE
  async getWeightCategories(): Promise<WeightCategory[]> {
    return request<WeightCategory[]>('/categories/weight');
  }
};
