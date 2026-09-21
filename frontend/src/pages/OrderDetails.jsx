import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getOrder } from "../api/orders";
import { confirmPayment } from "../api/payment";

export default function OrderDetails() {
  const { orderId } = useParams();

  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [paymentLoading, setPaymentLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadOrder() {
      try {
        const data = await getOrder(orderId);
        setOrder(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadOrder();
  }, [orderId]);

  async function handlePayment() {
    try {
      setPaymentLoading(true);
      setError("");

      const idempotencyKey = crypto.randomUUID();

      await confirmPayment(
        order.payment.id,
        idempotencyKey
      );

      const updatedOrder = await getOrder(orderId);

      setOrder(updatedOrder);
    } catch (error) {
      setError(error.message);
    } finally {
      setPaymentLoading(false);
    }
  }

  if (loading) {
    return <p>Loading order...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!order) {
    return <p>Order not found.</p>;
  }

  return (
    <div>
      <h1>Order #{order.id}</h1>

      <p>
        Restaurant: {order.restaurant_name}
      </p>

      <p>
        Status: {order.status}
      </p>

      <div>
        <h2>Order Progress</h2>
        <p>
          ✓ Order Placed
        </p>

        <p>
          {[
            "CONFIRMED",
            "PREPARING",
            "READY",
            "DRIVER_ASSIGNED",
            "PICKED_UP",
            "DELIVERED",
          ].includes(order.status)
            ? "✓ Restaurant Confirmed"
            : "○ Restaurant Confirmed"}
        </p>

        <p>
          {[
            "PREPARING",
            "READY",
            "DRIVER_ASSIGNED",
            "PICKED_UP",
            "DELIVERED",
          ].includes(order.status)
            ? "✓ Preparing"
            : "○ Preparing"}
        </p>

        <p>
          {[
            "READY",
            "DRIVER_ASSIGNED",
            "PICKED_UP",
            "DELIVERED",
          ].includes(order.status)
            ? "✓ Ready"
            : "○ Ready"}
        </p>

        <p>
          {[
            "DRIVER_ASSIGNED",
            "PICKED_UP",
            "DELIVERED",
          ].includes(order.status)
            ? "✓ Driver Assigned"
            : "○ Driver Assigned"}
        </p>

        <p>
          {[
            "PICKED_UP",
            "DELIVERED",
          ].includes(order.status)
            ? "✓ Picked Up"
            : "○ Picked Up"}
        </p>

        <p>
          {order.status === "DELIVERED"
            ? "✓ Delivered"
            : "○ Delivered"}
        </p>
      </div>

      <h2>Items</h2>

      {order.items?.map((item) => (
        <div key={item.id}>
          <p>
            {item.name_snapshot} × {item.quantity}
          </p>

          <p>
            ₹{item.subtotal}
          </p>
        </div>
      ))}

      <hr />

      <h2>
        Total: ₹{order.subtotal}
      </h2>

      <h2>Payment</h2>

      <p>
        Status: {order.payment?.status}
      </p>

      {order.payment?.status === "PENDING" && (
        <button
          onClick={handlePayment}
          disabled={paymentLoading}
        >
          {paymentLoading
            ? "Processing Payment..."
            : "Confirm Payment"}
        </button>
      )}

      {order.payment?.status === "SUCCESS" && (
        <p>Payment successful.</p>
      )}

      <br />

      <Link to="/orders">
        Back to Orders
      </Link>
    </div>
  );
}