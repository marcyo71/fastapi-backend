import React, { useEffect, useState } from 'react';

const BASE_URL = import.meta.env.PROD
  ? 'https://marcy-api.onrender.com'
  : '';

const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!userId) return;

    fetch(`${BASE_URL}/users/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error('Errore nel recupero utente');
        return res.json();
      })
      .then(setUser)
      .catch((err) => setError(err.message));
  }, [userId]);

  if (error) return <p className="text-red-500">❌ {error}</p>;
  if (!user) return <p>⏳ Caricamento utente...</p>;

  return (
    <div className="bg-white shadow-md rounded-md p-4">
      <h2 className="text-lg font-semibold mb-2">👤 Profilo Utente</h2>
      <p><strong>Nome:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>IBAN:</strong> {user.iban || 'Non disponibile'}</p>
    </div>
  );
};

export default UserProfile;
