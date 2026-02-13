import axios from "axios";

export const verifyOTP = async (email, otp) => {
  return axios.post(
    "http://localhost:8000/api/verify-otp/",
    {
      email: email,
      otp: otp.toString()   // ✅ MUST be string
    },
    {
      headers: {
        "Content-Type": "application/json"
      },
      withCredentials: true
    }
  );
};
