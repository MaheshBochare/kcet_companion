import { Navigate } from "react-router-dom";
import { useAuth } from "@/auth/AuthContext";

/**
 * ProtectedRoute
 * ----------------
 * - Blocks unauthenticated users
 * - Blocks users without required roles
 * - Waits for auth state to load
 *
 * Usage:
 * <ProtectedRoute roles={["USER", "OWNER"]}>
 *   <Home />
 * </ProtectedRoute>
 */
export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth();

  // ⏳ Wait until auth state is resolved
  if (loading) {
    return <p>Loading...</p>;
  }

  // ❌ Not logged in
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // ❌ Logged in but role not allowed
  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  // ✅ Access granted
  return children;
}
