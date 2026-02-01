import api from "./axios";

// ✅ SEND OTP (PUBLIC – NO CSRF)
export function sendOTP(email) {
  return api.post("auth/send-otp/", { email });
}

// ✅ VERIFY OTP (PUBLIC – NO CSRF)
export function verifyOTP(email, otp) {
  return api.post("auth/verify-otp/", { email, otp });
}

// ✅ RESEND OTP (PUBLIC – NO CSRF)
export function resendOTP(email) {
  return api.post("auth/resend-otp/", { email });
}

// ✅ LOGOUT (PROTECTED)
export function logout(refresh) {
  return api.post("auth/logout/", { refresh });
}
