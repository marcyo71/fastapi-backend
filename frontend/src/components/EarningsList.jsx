import React, { useEffect, useState } from "react";

export default function EarningsList({ userId }) {
  const [earnings, setEarnings] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!userId) return;
    fetch(`/api/earnings/${userId}`)
      .then(res => res.json())
      .then(data => setEarnings(data.earnings))
      .catch(err => setError(err.message));
  }, [userId]);

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">Lista Guadagni Utente {userId}</h2>
      {error && <p className="text-red-500 mb-2">Errore: {error}</p>}
      {earnings.length === 0 && !error ? (
        <p className="text-gray-600">Nessun guadagno registrato.</p>
      ) : (
        <ul className="list-disc pl-5 space-y-1">
          {earnings.map((e, i) => (
            <li key={i} className="text-gray-800">
              {e} EUR
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
