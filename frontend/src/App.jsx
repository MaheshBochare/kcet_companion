import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

/* ---------- Pages ---------- */
import Home from "./pages/Home";
import Cutoff from "./pages/cutoff";
import Seatmatrix from "./pages/seatmatrix";

/* ---------- Auth Pages ---------- */
import Login from "./pages/Login";
import VerifyOTP from "./pages/VerifyOTP";
import Unauthorized from "./pages/Unauthorized";

/* ---------- Dashboards ---------- */
import OwnerDashboard from "./pages/OwnerDashboard";

/* ---------- Auth System ---------- */
import { AuthProvider } from "@/auth/AuthContext";
import ProtectedRoute from "@/auth/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>

          {/* ---------- Public Auth ---------- */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/verify-otp" element={<VerifyOTP />} />

          {/* ---------- USER & OWNER ---------- */}
          <Route
            path="/home"
            element={
              <ProtectedRoute roles={["USER", "OWNER"]}>
                <Home />
              </ProtectedRoute>
            }
          />

          <Route
            path="/cutoff"
            element={
              <ProtectedRoute roles={["USER", "OWNER"]}>
                <Cutoff />
              </ProtectedRoute>
            }
          />

          <Route
            path="/seatmatrix"
            element={
              <ProtectedRoute roles={["USER", "OWNER"]}>
                <Seatmatrix />
              </ProtectedRoute>
            }
          />

          {/* ---------- OWNER ONLY ---------- */}
          <Route
            path="/owner"
            element={
              <ProtectedRoute roles={["OWNER"]}>
                <OwnerDashboard />
              </ProtectedRoute>
            }
          />

          {/* ---------- Unauthorized ---------- */}
          <Route path="/unauthorized" element={<Unauthorized />} />

          {/* ---------- Fallback ---------- */}
          <Route path="*" element={<Navigate to="/login" replace />} />

        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
