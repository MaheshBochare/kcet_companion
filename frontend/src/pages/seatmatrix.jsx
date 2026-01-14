import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function SeatMatrix() {
  const [data, setData] = useState([]);

  useEffect(() => {
    api.get("/seatmatrix/").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h2>Seat Matrix</h2>
      <table>
        <thead>
          <tr>
            <th>College</th>
            <th>Branch</th>
            <th>Category</th>
            <th>Total</th>
            <th>Available</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r, i) => (
            <tr key={i}>
              <td>{r.college}</td>
              <td>{r.branch}</td>
              <td>{r.category}</td>
              <td>{r.total_seats}</td>
              <td>{r.available_seats}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
