import { useAuth } from "../auth/useAuth";

export default function AdminDashboard() {
  const { user } = useAuth();

  return (
    <div style={{ padding: "24px" }}>
      <h2>Admin Dashboard</h2>

      <p>
        Logged in as <strong>{user?.email}</strong>
      </p>

      <p>Role: {user?.role}</p>

      <hr />

      <ul>
        <li>Approve user emails</li>
        <li>Manage allowed users</li>
        <li>View system usage</li>
      </ul>
    </div>
  );
}
