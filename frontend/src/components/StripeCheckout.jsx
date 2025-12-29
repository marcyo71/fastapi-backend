import React, { useState } from "react";

export default function StripeCheckout() {
  const [loading, setLoading] = useState(false);

  // --- STRIPE CHECKOUT ---
  const handleStripeCheckout = async () => {
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/stripe/create-payment-intent", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    amount: 4990,   // in centesimi
    currency: "eur"
  }),
});

      const data = await res.json();

      // Se usi Stripe.js, qui useresti client_secret per confermare il pagamento
      console.log("Client secret:", data.client_secret);

      // Oppure se usi Checkout Session, fai redirect a data.checkout_url
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      }
    } catch (err) {
      console.error("Errore Stripe:", err);
      setLoading(false);
    }
  };

  // --- KLARNA CHECKOUT ---
  const handleKlarnaCheckout = async () => {
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/checkout/klarna", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const data = await res.json();
      window.location.href = data.checkout_url;
    } catch (err) {
      console.error("Errore Klarna:", err);
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>💳 Checkout</h2>

      <button onClick={handleStripeCheckout} disabled={loading}>
        {loading ? "⌛ Attendi…" : "Paga con Stripe"}
      </button>

      <br /><br />

      <button onClick={handleKlarnaCheckout} disabled={loading}>
        {loading ? "⌛ Attendi…" : "Paga con Klarna"}
      </button>
    </div>
  );
}
