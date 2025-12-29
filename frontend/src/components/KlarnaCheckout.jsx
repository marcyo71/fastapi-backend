// src/components/KlarnaCheckout.jsx
import React, { useEffect, useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import { Elements, useStripe, useElements, PaymentElement } from "@stripe/react-stripe-js";

// Carica la chiave pubblica Stripe dal tuo .env
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

// URL del backend FastAPI
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function KlarnaForm({ clientSecret }) {
  const stripe = useStripe();
  const elements = useElements();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!stripe || !elements) return;

    setIsSubmitting(true);
    setMessage("");

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/dashboard`, // redirect dopo pagamento
      },
    });

    if (error) {
      setMessage(error.message || "Errore durante il pagamento.");
      setIsSubmitting(false);
    } else {
      setMessage("Reindirizzamento a Klarna in corso...");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 480, margin: "2rem auto" }}>
      <PaymentElement />
      <button
        type="submit"
        disabled={!stripe || !elements || isSubmitting}
        style={{
          marginTop: "1rem",
          padding: "0.75rem 1rem",
          background: "#000",
          color: "#fff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        {isSubmitting ? "Elaborazione..." : "Paga con Klarna"}
      </button>
      {message && <div style={{ marginTop: "0.75rem", color: "#c00" }}>{message}</div>}
    </form>
  );
}

export default function KlarnaCheckout() {
  const [clientSecret, setClientSecret] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const createIntent = async () => {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE}/api/stripe/create-payment-intent`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            amount: 5000, // €50.00
            currency: "eur",
            payment_method_types: ["klarna"],
          }),
        });
        if (!res.ok) {
          const data = await res.json().catch(() => ({}));
          throw new Error(data.detail || "Errore nella creazione del PaymentIntent");
        }
        const data = await res.json();
        setClientSecret(data.client_secret);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    createIntent();
  }, []);

  if (loading) return <div style={{ padding: "2rem", textAlign: "center" }}>Preparazione pagamento…</div>;
  if (error) return <div style={{ padding: "2rem", color: "#c00" }}>Errore: {error}</div>;
  if (!clientSecret) return <div style={{ padding: "2rem", color: "#c00" }}>Nessun client_secret ricevuto.</div>;

  const options = {
    clientSecret,
    appearance: { theme: "stripe" },
  };

  return (
    <Elements stripe={stripePromise} options={options}>
      <KlarnaForm clientSecret={clientSecret} />
    </Elements>
  );
}
