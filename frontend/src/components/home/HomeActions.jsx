import { Link } from "react-router-dom";

export default function HomeActions() {
  return (
    <div className="action-buttons">
      <Link to="/cutoff" className="btn btn-primary action-btn">
        <i className="fas fa-chart-line me-2"></i>
        Cutoff Analyzer
      </Link>

      <Link to="/seatmatrix" className="btn btn-primary action-btn">
        <i className="fas fa-chair me-2"></i>
        Seat Matrix
      </Link>

      <Link to="/predictor" className="btn btn-primary action-btn">
        <i className="fas fa-calculator me-2"></i>
        Predictor
      </Link>
    </div>
  );
}
