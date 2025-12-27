import React, { useState } from "react";

export default function EarningsForm({ userId }) {
  const [amount, setAmount] = useState("");
  const [currency, setCurrency] = useState("EUR");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const res = await fetch(`/api/earnings/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount: Number(amount), currency }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Errore ${res.status}: ${text}`);
      }

      setSuccess("Guadagno registrato con successo!");
      setAmount("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">Aggiungi Guadagno</h2>
      {error && <p className="text-red-500 mb-2">Errore: {error}</p>}
      {success && <p className="text-green-600 mb-2">{success}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium mb-1">
            Importo:
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="border rounded px-2 py-1 w-full"
              required
            />
          </label>
        </div>
        <div>
          <label className="block font-medium mb-1">
            Valuta:
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="border rounded px-2 py-1 w-full"
            >
              <option value="EUR">EUR</option>
              <option value="USD">USD</option>
            </select>
          </label>
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Registra
        </button>
      </form>
    </div>
  );
}
