import React from 'react';
import { api, Profile } from '../api/client';
import CandidateCard from '../components/CandidateCard';
import FilterPanel from '../components/FilterPanel';

export default function CandidatesPage() {
  const [filters, setFilters] = React.useState<{ height_category_id: number | null; weight_category_id: number | null }>({
    height_category_id: null,
    weight_category_id: null
  });
  const [items, setItems] = React.useState<Profile[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [accepted, setAccepted] = React.useState<Set<number>>(new Set());
  const [rejected, setRejected] = React.useState<Set<number>>(new Set());

  const load = React.useCallback(() => {
    setLoading(true);
    setError(null);
    api
      .listProfiles(filters)
      .then((data) => setItems(data))
      .catch((e) => setError(e.message || String(e)))
      .finally(() => setLoading(false));
  }, [filters]);

  React.useEffect(() => {
    load();
  }, [load]);

  const onAccept = (id: number) => {
    setAccepted((prev) => new Set(prev).add(id));
  };

  const onReject = (id: number) => {
    setRejected((prev) => new Set(prev).add(id));
  };

  const visible = items.filter((p) => !accepted.has(p.id) && !rejected.has(p.id));

  return (
    <div className="stack">
      <FilterPanel value={filters} onChange={setFilters} />
      <div className="panel">
        <div className="panel-title row-between">
          <span>Candidates</span>
          <button className="btn btn-sm" onClick={load} disabled={loading}>Refresh</button>
        </div>
        {loading && <div className="muted">Loading...</div>}
        {error && <div className="error">Error: {error}</div>}
        {!loading && !error && visible.length === 0 && (
          <div className="muted">No candidates. Try adjusting filters.</div>
        )}
        <div className="grid-cards">
          {visible.map((p) => (
            <CandidateCard key={p.id} profile={p} onAccept={onAccept} onReject={onReject} />
          ))}
        </div>
      </div>
    </div>
  );
}
