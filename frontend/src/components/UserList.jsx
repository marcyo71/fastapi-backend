import React, { useEffect, useState } from 'react';

const UserList = ({ refreshTrigger }) => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  const fetchUsers = () => {
    fetch('/users')
      .then((res) => {
        if (!res.ok) throw new Error('Errore nel recupero utenti');
        return res.json();
      })
      .then((data) => setUsers(data))
      .catch((err) => setError(err.message));
  };

  useEffect(() => {
    fetchUsers();
  }, [refreshTrigger]);

  if (error) return <div>Errore: {error}</div>;
  if (!users.length) return <div>Nessun utente trovato.</div>;

  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px', marginTop: '1rem' }}>
      <h2>👥 Utenti registrati</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <strong>{user.name}</strong> — {user.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
<ul>
  {users.map((user) => (
    <li key={user.id} className="border-b py-2">
      <strong>{user.name}</strong> — {user.email}
      <br />
      <span className="text-sm text-gray-600">IBAN: {user.iban || 'Non disponibile'}</span>
    </li>
  ))}
</ul>
