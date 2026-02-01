import { Link } from "react-router-dom";
import "@/styles/cutoff.css";

export default function DashboardLayout({ children }) {
  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <h3 className="logo">KCET Portal</h3>

        <nav>
          <Link to="/">🏠 Home</Link>
          <Link to="/seatmatrix">🪑 Seat Matrix</Link>
          <Link to="/predictor">🧮 Predictor</Link>
          <Link to="/cutoff">📊 Cutoff Analyzer</Link>
        </nav>
      </aside>

      {/* Main Area */}
      <div className="main">
        <header className="header">
          <h2>KCET Engineering Admission Analytics 
            Cutoff-Analyzer
          </h2>
        </header>

        <section className="content">{children}</section>

        <footer className="footer">
          © 2026 KCET Admission Portal
        </footer>
      </div>
    </div>
  );
}
