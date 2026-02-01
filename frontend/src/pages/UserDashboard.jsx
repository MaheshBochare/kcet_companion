import { useAuth } from "../auth/useAuth";

export default function UserDashboard() {
  const { user } = useAuth();

  return (
    <div style={{ padding: "24px" }}>
      <h2>User Dashboard</h2>

      <p>
        Welcome <strong>{user?.email}</strong>
      </p>

      <p>Role: {user?.role}</p>

      <hr />

      <p>You have access to KCET analytics and tools.</p>
    </div>
  );
}
