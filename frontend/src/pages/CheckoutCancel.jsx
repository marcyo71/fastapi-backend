import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function CheckoutCancel() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/checkout");
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="p-10 text-center">
      <h1 className="text-3xl font-bold text-red-600">Pagamento annullato</h1>
      <p className="mt-4">Verrai reindirizzato…</p>
    </div>
  );
}
