import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { checkout } from "../api/orders";

export default function Checkout() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  async function handleCheckout() {
    try {
      setLoading(true);
      setError("");

      const order = await checkout();
      navigate(`/orders/${order.id}`);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
      <div className="mx-auto max-w-xl rounded-[30px] border border-slate-200 bg-white p-8 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
        <h1 className="text-3xl font-black tracking-[-0.08em] text-slate-900">Checkout</h1>
        <p className="mt-3 text-slate-600">
          Your order will be created and a payment will be created with status PENDING.
        </p>

        {error && (
          <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 px-3 py-2 text-sm font-medium text-red-700">
            {error}
          </div>
        )}

        <button
          type="button"
          className="mt-6 w-full rounded-2xl bg-gradient-to-r from-brand-500 to-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70"
          onClick={handleCheckout}
          disabled={loading}
        >
          {loading ? "Processing..." : "Place Order"}
        </button>
      </div>
    </div>
  );
}