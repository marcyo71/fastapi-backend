import React, { useState } from 'react';

const BASE_URL = import.meta.env.PROD
  ? 'https://your-backend.onrender.com' // 🔁 Sostituisci con il tuo URL reale
  : '';

const IBANForm = ({ userId, currentIban, onSuccess }) => {
  const [iban, setIban] = useState(currentIban || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${BASE_URL}/users/${userId}/iban`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ iban }),
      });

      if (!res.ok) throw new Error('Errore durante l’aggiornamento dell’IBAN');
      onSuccess && onSuccess(); // callback per aggiornare il profilo
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 space-y-2">
      <label className="block text-sm font-medium">Modifica IBAN</label>
      <input
        type="text"
        value={iban}
        onChange={(e) => setIban(e.target.value)}
        className="border rounded px-2 py-1 w-full"
        placeholder="Inserisci nuovo IBAN"
      />
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
      >
        {loading ? 'Salvataggio...' : 'Salva IBAN'}
      </button>
    </form>
  );
};

export default IBANForm;
