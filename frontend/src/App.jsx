import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Cutoff from "./pages/Cutoff";
import Seatmatrix from "./pages/seatmatrix";  

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cutoff" element={<Cutoff />} />
        <Route path="/seatmatrix" element={<Seatmatrix />} />
      </Routes>
    </BrowserRouter>
    
  );
}
