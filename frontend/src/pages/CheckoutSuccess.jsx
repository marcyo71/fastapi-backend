import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function CheckoutSuccess() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/");
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="p-10 text-center">
      <h1 className="text-3xl font-bold text-green-600">Pagamento riuscito!</h1>
      <p className="mt-4">Grazie per il tuo ordine. Verrai reindirizzato…</p>
    </div>
  );
}
