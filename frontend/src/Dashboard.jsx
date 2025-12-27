import { useEffect, useState } from "react";

export default function Dashboard() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/dashboard/events")
      .then(res => res.json())
      .then(data => setEvents(data));
  }, []);

  return (
    <div>
      <h2>Eventi Stripe</h2>
      <ul>
        {events.map((e, i) => (
          <li key={i}>{e.type} – {e.timestamp}</li>
        ))}
      </ul>
    </div>
  );
}
