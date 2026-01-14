import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2>KCET Companion</h2>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/seatmatrix">Seat Matrix</Link>
        <Link to="/cutoff">Cutoff</Link>
        <Link to="/predictor">Predictor</Link>
      </nav>
    </div>
  );
}
