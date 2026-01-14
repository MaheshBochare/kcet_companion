import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Cutoff from "./pages/Cutoff";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cutoff" element={<Cutoff />} />
      </Routes>
    </BrowserRouter>
  );
}
