import React, { useEffect, useState } from "react";

export default function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!userId) return;
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data))
      .catch(err => setError(err.message));
  }, [userId]);

  if (error) {
    return (
      <div className="p-4 bg-white shadow rounded">
        <h2 className="text-xl font-bold mb-2">Profilo Utente</h2>
        <p className="text-red-500">Errore: {error}</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="p-4 bg-white shadow rounded">
        <h2 className="text-xl font-bold mb-2">Profilo Utente</h2>
        <p>Caricamento...</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-2">Profilo Utente</h2>
      <p><span className="font-semibold">ID:</span> {user.id}</p>
      <p><span className="font-semibold">Nome:</span> {user.name}</p>
    </div>
  );
}
