import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { sendOTP, verifyOTP } from "../api/auth.api";
import { useAuth } from "@/auth/AuthContext";
import "../styles/login.css";

const OTP_EXPIRY = 120;
const RESEND_DELAY = 30;

export default function Login() {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState("EMAIL");
  const [otpTimer, setOtpTimer] = useState(OTP_EXPIRY);
  const [resendTimer, setResendTimer] = useState(0);
  const [loading, setLoading] = useState(false);

  const { user, login } = useAuth();
  const navigate = useNavigate();

  /* Redirect if already logged in */
  useEffect(() => {
    if (user) navigate("/home", { replace: true });
  }, [user, navigate]);

  /* Particles background */
  useEffect(() => {
    if (window.particlesJS) {
      window.particlesJS("particles-js", {
        particles: { number: { value: 60 } }
      });
    }
  }, []);

  /* OTP expiry countdown */
  useEffect(() => {
    if (step === "OTP" && otpTimer > 0) {
      const t = setInterval(() => setOtpTimer(v => v - 1), 1000);
      return () => clearInterval(t);
    }
  }, [otpTimer, step]);

  /* Resend cooldown */
  useEffect(() => {
    if (resendTimer > 0) {
      const t = setInterval(() => setResendTimer(v => v - 1), 1000);
      return () => clearInterval(t);
    }
  }, [resendTimer]);

  const requestOtp = async () => {
    if (!email.trim()) return alert("Enter email");
    try {
      setLoading(true);
      await sendOTP(email);
      setStep("OTP");
      setOtp("");
      setOtpTimer(OTP_EXPIRY);
      setResendTimer(RESEND_DELAY);
    } catch {
      alert("Failed to send OTP");
    } finally {
      setLoading(false);
    }
  };

  const verifyOtp = async () => {
    if (!otp.trim()) return alert("Enter OTP");
    try {
      setLoading(true);
      const res = await verifyOTP(email, otp);
      login({ email, role: res.data.role });
      navigate("/home", { replace: true });
    } catch {
      alert("Invalid OTP");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      {/* Particles */}
      <div id="particles-js"></div>

      {/* Floating element */}
      <div className="floating"></div>

      {/* Header */}
      <header>
        <div className="logo">
          <i className="fas fa-graduation-cap"></i>
          <span>KCET Companion</span>
        </div>
        <nav>
          <a href="#">Home</a>
          <a href="#">Features</a>
        </nav>
      </header>

      {/* Centered Login */}
      <div className="page-center">
        <div className="login-container">
          <h2>Welcome Back</h2>

          {/* Email */}
          <div className="input-group">
            <label>Email</label>
            <i className="fas fa-envelope input-icon"></i>
            <input
              type="email"
              value={email}
              disabled={step === "OTP"}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>

          {/* OTP */}
          {step === "OTP" && (
            <div className="input-group">
              <label>OTP</label>
              <i className="fas fa-lock input-icon"></i>
              <input
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="Enter OTP"
              />
              <div className="otp-timer">
                Expires in {otpTimer}s
              </div>
            </div>
          )}

          {/* Buttons */}
          {step === "EMAIL" && (
            <button
              className="button"
              onClick={requestOtp}
              disabled={loading}
            >
              {loading ? "Sending OTP..." : "Request OTP"}
            </button>
          )}

          {step === "OTP" && (
            <>
              <button
                className="button"
                onClick={verifyOtp}
                disabled={loading}
              >
                {loading ? "Verifying..." : "Login"}
              </button>

              <button
                className="button"
                disabled={resendTimer > 0 || loading}
                onClick={requestOtp}
              >
                {resendTimer
                  ? `Resend in ${resendTimer}s`
                  : "Resend OTP"}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer>
        © 2024 KCET Companion
      </footer>
    </div>
  );
}
