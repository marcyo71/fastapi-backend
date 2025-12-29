import React, { useState } from "react";

export default function IBANForm({ userId }) {
  const [iban, setIban] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const res = await fetch(`/api/iban/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ iban }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Errore ${res.status}: ${text}`);
      }

      setSuccess("IBAN registrato con successo!");
      setIban("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">Aggiungi IBAN</h2>
      {error && <p className="text-red-500 mb-2">Errore: {error}</p>}
      {success && <p className="text-green-600 mb-2">{success}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium mb-1">
            IBAN:
            <input
              type="text"
              value={iban}
              onChange={(e) => setIban(e.target.value)}
              className="border rounded px-2 py-1 w-full"
              placeholder="IT60X0542811101000000123456"
              required
            />
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
