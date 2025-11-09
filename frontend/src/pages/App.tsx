import { Outlet } from 'react-router-dom';
import Header from '../components/Header';

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="container main">
        <Outlet />
      </main>
      <footer className="footer">
        <div className="container muted small">© {new Date().getFullYear()} MatchFilter • Demo Frontend</div>
      </footer>
    </div>
  );
}
