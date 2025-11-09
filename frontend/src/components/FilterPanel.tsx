import React from 'react';
import { api, HeightCategory, WeightCategory } from '../api/client';

type Props = {
  value: { height_category_id: number | null; weight_category_id: number | null };
  onChange: (v: { height_category_id: number | null; weight_category_id: number | null }) => void;
};

export default function FilterPanel({ value, onChange }: Props) {
  const [heightCats, setHeightCats] = React.useState<HeightCategory[]>([]);
  const [weightCats, setWeightCats] = React.useState<WeightCategory[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    let ignore = false;
    setLoading(true);
    Promise.all([api.getHeightCategories(), api.getWeightCategories()])
      .then(([h, w]) => {
        if (ignore) return;
        setHeightCats(h);
        setWeightCats(w);
      })
      .catch((e) => {
        if (ignore) return;
        setError(e.message || String(e));
      })
      .finally(() => {
        if (ignore) return;
        setLoading(false);
      });
    return () => { ignore = true; };
  }, []);

  return (
    <section className="panel">
      <div className="panel-title">Filters</div>
      {loading && <div className="muted">Loading categories...</div>}
      {error && <div className="error">Error: {error}</div>}
      <div className="grid">
        <label className="field">
          <span className="label">Height Category</span>
          <select
            value={value.height_category_id ?? ''}
            onChange={(e) =>
              onChange({
                ...value,
                height_category_id: e.target.value ? Number(e.target.value) : null
              })
            }
          >
            <option value="">Any</option>
            {heightCats.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          <span className="label">Weight Category</span>
          <select
            value={value.weight_category_id ?? ''}
            onChange={(e) =>
              onChange({
                ...value,
                weight_category_id: e.target.value ? Number(e.target.value) : null
              })
            }
          >
            <option value="">Any</option>
            {weightCats.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
      </div>
    </section>
  );
}
