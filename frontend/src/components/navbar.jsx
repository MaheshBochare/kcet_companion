import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  // ✅ ADD THIS LINE HERE
  const isLoggedIn = !!localStorage.getItem("accessToken");

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <nav className="nav">
      <h2>KCET Companion</h2>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/chat">Chatbot</Link>
        <Link to="/predict">Predictor</Link>

        {/* ✅ ADD THIS BLOCK HERE */}
        {isLoggedIn && (
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}
