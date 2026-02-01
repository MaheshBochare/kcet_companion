import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { verifyOTP, sendOTP } from "../api/auth.api";
import { useAuth } from "@/auth/AuthContext";

export default function VerifyOTP() {
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { user, login } = useAuth();

  const email = localStorage.getItem("loginEmail");

  // 🔒 Block invalid access
  useEffect(() => {
    // Already logged in → go home
    if (user) {
      navigate("/home", { replace: true });
    }

    // Direct access without email → go login
    if (!email) {
      navigate("/login", { replace: true });
    }
  }, [user, email, navigate]);

  const submit = async () => {
    if (!otp.trim()) {
      alert("OTP is required");
      return;
    }

    try {
      setLoading(true);

      const res = await verifyOTP(email, otp);

      // ✅ Save user in AuthContext
      login({
        email,
        role: res.data.role,
      });

      // Clear OTP flow state
      localStorage.removeItem("loginEmail");

      // 🧭 Role-based redirect
      if (res.data.role === "ADMIN") {
        window.location.href = "http://localhost:8000/admin/";
      } else {
        navigate("/home", { replace: true }); // USER & OWNER
      }

    } catch (err) {
      alert(err.response?.data?.error || "OTP verification failed");
    } finally {
      setLoading(false);
    }
  };

  const resendOTP = async () => {
    try {
      await sendOTP(email);
      alert("OTP resent successfully");
    } catch {
      alert("Failed to resend OTP");
    }
  };

  return (
    <div>
      <h2>Verify OTP</h2>

      <input
        placeholder="Enter OTP"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
      />

      <button onClick={submit} disabled={loading}>
        {loading ? "Verifying..." : "Verify OTP"}
      </button>

      <br />

      <button onClick={resendOTP} disabled={loading}>
        Resend OTP
      </button>
    </div>
  );
}
