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
    <div>
      <h1>Checkout</h1>

      <p>
        Your order will be created and a payment will be
        created with status PENDING.
      </p>

      {error && <p>{error}</p>}

      <button
        onClick={handleCheckout}
        disabled={loading}
      >
        {loading ? "Processing..." : "Place Order"}
      </button>
    </div>
  );
}