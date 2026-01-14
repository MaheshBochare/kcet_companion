import { useState } from "react";
import { api } from "../api/client";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    const res = await api.post("/chatbot/", { message: input });
    setMessages([...messages, { user: input }, { bot: res.data.reply }]);
    setInput("");
  }

  return (
    <div className="chat">
      {messages.map((m, i) => (
        <p key={i}><b>{m.user ? "You" : "Bot"}:</b> {m.user || m.bot}</p>
      ))}
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
