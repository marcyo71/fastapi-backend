import React, { useEffect, useState } from "react";

export default function UserList() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/users")
      .then(res => res.json())
      .then(data => setUsers(data.users || []))
      .catch(err => setError(err.message));
  }, []);

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-2">Lista Utenti</h2>
      {error && <p className="text-red-500">Errore: {error}</p>}
      {users.length === 0 && !error ? (
        <p>Nessun utente.</p>
      ) : (
        <ul className="list-disc pl-5">
          {users.map(u => (
            <li key={u.id}>
              {u.id} - {u.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
