import React, { useEffect, useState } from "react";

export default function UserForm() {
  const [stripeKey, setStripeKey] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/stripe/public-key")
      .then(res => res.json())
      .then(data => setStripeKey(data.public_key))
      .catch(err => setError(err.message));
  }, []);

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-2">Form Utente</h2>
      {error && <p className="text-red-500">Errore: {error}</p>}
      <p>
        <span className="font-semibold">Chiave Pubblica Stripe:</span>{" "}
        {stripeKey || "Nessuna chiave"}
      </p>
    </div>
  );
}
