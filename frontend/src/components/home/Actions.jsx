import { Link } from "react-router-dom";

export default function HomeActions() {
  return (
    <div className="text-center my-4">
      <Link to="/cutoff" className="btn btn-primary btn-lg me-2">Cutoff Analyzer</Link>
      <Link to="/seat" className="btn btn-primary btn-lg me-2">Seat Matrix</Link>
      <Link to="/predictor" className="btn btn-primary btn-lg">Predictor</Link>
    </div>
  );
}
