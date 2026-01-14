import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="nav">
      <h2>KCET Companion</h2>
      <div>
        <Link to="/">Home</Link>
        <Link to="/chat">Chatbot</Link>
        <Link to="/predict">Predictor</Link>
      </div>
    </nav>
  );
}
