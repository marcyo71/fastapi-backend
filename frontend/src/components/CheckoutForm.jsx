import { useState } from "react";
import { useStripe, useElements, PaymentElement } from "@stripe/react-stripe-js";

export default function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    if (!stripe || !elements) {
      setMessage("Stripe non è pronto.");
      setLoading(false);
      return;
    }

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: "http://localhost:5173/success",
      },
    });

    if (error) {
      setMessage(error.message);
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: "400px" }}>
      <PaymentElement />

      {message && (
        <p style={{ color: "red", marginTop: "10px" }}>{message}</p>
      )}

      <button
        disabled={!stripe || loading}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          background: "#635bff",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          opacity: loading ? 0.6 : 1,
        }}
      >
        {loading ? "Elaborazione…" : "Paga ora"}
      </button>
    </form>
  );
}
