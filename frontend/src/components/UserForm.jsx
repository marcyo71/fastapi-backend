import React, { useState } from 'react';

const UserForm = ({ onUserAdded }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);

    try {
      const res = await fetch(`/users?name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}`, {
        method: 'POST',
      });

      if (!res.ok) throw new Error('Errore nella creazione utente');
      const data = await res.json();
      setMessage(`✅ Utente creato: ${data.name} (${data.email})`);
      setName('');
      setEmail('');
      onUserAdded(); // 🔄 trigger refresh
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px', marginTop: '1rem' }}>
      <h2>➕ Aggiungi Utente</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nome:</label><br />
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div>
          <label>Email:</label><br />
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <button type="submit" style={{ marginTop: '0.5rem' }}>Aggiungi</button>
      </form>
      {message && <p style={{ marginTop: '1rem' }}>{message}</p>}
    </div>
  );
};

export default UserForm;
<form onSubmit={handleSubmit} className="bg-white shadow-md rounded-md p-4 space-y-4">
  <div>
    <label className="block text-sm font-medium text-gray-700">Nome</label>
    <input
      type="text"
      value={name}
      onChange={(e) => setName(e.target.value)}
      required
      className="mt-1 block w-full border border-gray-300 rounded-md p-2"
    />
  </div>
  <div>
    <label className="block text-sm font-medium text-gray-700">Email</label>
    <input
      type="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      required
      pattern="^[^@\s]+@[^@\s]+\.[^@\s]+$"
      className="mt-1 block w-full border border-gray-300 rounded-md p-2"
    />
  </div>
  <button type="submit" className="bg-primary text-white px-4 py-2 rounded-md hover:bg-blue-700">
    Aggiungi
  </button>
  {message && <p className="text-sm mt-2">{message}</p>}
</form>
