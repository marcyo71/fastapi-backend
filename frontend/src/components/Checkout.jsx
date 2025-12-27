import { useEffect } from "react";

export default function Checkout() {
  useEffect(() => {
    fetch("http://localhost:8000/api/checkout/create-checkout-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then(res => res.json())
      .then(data => {
        window.location.href = data.url;
      })
      .catch(err => console.error("Errore checkout:", err));
  }, []);

  return <p>Reindirizzamento in corso…</p>;
}
