import React, { useEffect, useState } from 'react';

const EarningsList = ({ userId }) => {
  const [earnings, setEarnings] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!userId) return;

    fetch(`/users/${userId}/earnings`)
      .then((res) => {
        if (!res.ok) throw new Error('Errore nel recupero guadagni');
        return res.json();
      })
      .then((data) => setEarnings(data))
      .catch((err) => setError(err.message));
  }, [userId]);

  if (!userId) return <div>Seleziona un utente per vedere i guadagni.</div>;
  if (error) return <div>Errore: {error}</div>;
  if (!earnings.length) return <div>Nessun guadagno registrato.</div>;

  return (
    <div className="bg-white shadow-md rounded-md p-4 mt-4">
      <h2 className="text-lg font-semibold mb-2">💰 Guadagni utente #{userId}</h2>
      <ul className="space-y-2">
        {earnings.map((e) => (
          <li key={e.id} className="text-sm">
            {e.amount} {e.currency} — <em>{new Date(e.timestamp).toLocaleString()}</em>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EarningsList;
import EarningsList from './components/EarningsList';
import { useState } from 'react';

function App() {
  const [selectedUserId, setSelectedUserId] = useState(null);

  return (
    <div>
      <h1>Dashboard</h1>
      <button onClick={() => setSelectedUserId(1)}>Mostra guadagni utente #1</button>
      <EarningsList userId={selectedUserId} />
    </div>
  );
}
import { fetchUserEarnings } from '../api/api';

useEffect(() => {
  if (!userId) return;
  fetchUserEarnings(userId)
    .then(setEarnings)
    .catch((err) => setError(err.message));
}, [userId]);
