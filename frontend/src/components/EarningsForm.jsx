import React, { useState } from 'react';

const EarningsForm = ({ userId, onEarningAdded }) => {
  const [amount, setAmount] = useState('');
  const [currency, setCurrency] = useState('EUR');
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);

    try {
      const res = await fetch(`/earnings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          amount: parseFloat(amount),
          currency,
        }),
      });

      if (!res.ok) throw new Error('Errore nell’aggiunta guadagno');
      const data = await res.json();
      setMessage(`✅ Guadagno registrato: ${data.amount} ${data.currency}`);
      setAmount('');
      setCurrency('EUR');
      onEarningAdded?.(); // 🔄 trigger refresh se fornito
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-md p-4 mt-4 space-y-4">
      <h2 className="text-lg font-semibold">➕ Aggiungi Guadagno</h2>
      <div>
        <label className="block text-sm font-medium text-gray-700">Importo</label>
        <input
          type="number"
          step="0.01"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md p-2"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Valuta</label>
        <select
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md p-2"
        >
          <option value="EUR">EUR</option>
          <option value="USD">USD</option>
          <option value="GBP">GBP</option>
        </select>
      </div>
      <button type="submit" className="bg-primary text-white px-4 py-2 rounded-md hover:bg-blue-700">
        Registra
      </button>
      {message && <p className="text-sm mt-2">{message}</p>}
    </form>
  );
};

export default EarningsForm;
import { addEarning } from '../api/api';

await addEarning({ user_id: userId, amount: parseFloat(amount), currency });
