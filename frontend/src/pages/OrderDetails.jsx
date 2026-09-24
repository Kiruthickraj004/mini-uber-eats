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
      const paymentId = order?.payment?.id ?? order?.payment_id;

      if (!paymentId) {
        throw new Error("Payment information is not available for this order.");
      }

      await confirmPayment(paymentId, idempotencyKey);
      const updatedOrder = await getOrder(orderId);
      setOrder(updatedOrder);
    } catch (error) {
      setError(error.message);
    } finally {
      setPaymentLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
          Loading order...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
          Order not found.
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900">Order #{order.id}</h1>
        <p className="mt-2 text-slate-600">Restaurant: {order.restaurant_name}</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[30px] border border-slate-200 bg-white p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
          <h2 className="text-2xl font-black tracking-[-0.05em] text-slate-900">Order Progress</h2>
          <div className="mt-5 space-y-3">
            {[
              { label: "Order Placed", active: true },
              { label: "Restaurant Confirmed", active: ["CONFIRMED", "PREPARING", "READY", "DRIVER_ASSIGNED", "PICKED_UP", "DELIVERED"].includes(order.status) },
              { label: "Preparing", active: ["PREPARING", "READY", "DRIVER_ASSIGNED", "PICKED_UP", "DELIVERED"].includes(order.status) },
              { label: "Ready", active: ["READY", "DRIVER_ASSIGNED", "PICKED_UP", "DELIVERED"].includes(order.status) },
              { label: "Driver Assigned", active: ["DRIVER_ASSIGNED", "PICKED_UP", "DELIVERED"].includes(order.status) },
              { label: "Picked Up", active: ["PICKED_UP", "DELIVERED"].includes(order.status) },
              { label: "Delivered", active: order.status === "DELIVERED" },
            ].map((step) => (
              <div key={step.label} className={`flex items-center gap-3 rounded-2xl px-3 py-2 ${step.active ? "bg-brand-50 text-brand-800" : "bg-slate-50 text-slate-500"}`}>
                <span className={`h-2.5 w-2.5 rounded-full ${step.active ? "bg-brand-500" : "bg-slate-300"}`} />
                <span className="font-medium">{step.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-[30px] border border-slate-200 bg-white p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
          <h2 className="text-2xl font-black tracking-[-0.05em] text-slate-900">Payment</h2>
          <p className="mt-4 text-slate-600">Status: {order.payment?.status}</p>
          {order.payment?.status === "PENDING" && (
            <button type="button" className="mt-5 inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70" onClick={handlePayment} disabled={paymentLoading}>
              {paymentLoading ? "Processing Payment..." : "Confirm Payment"}
            </button>
          )}
          {order.payment?.status === "SUCCESS" && (
            <div className="mt-5 rounded-2xl border border-brand-200 bg-brand-50 px-3 py-2 text-sm font-medium text-brand-800">
              Payment successful.
            </div>
          )}
        </div>
      </div>

      <div className="mt-6 rounded-[30px] border border-slate-200 bg-white p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
        <h2 className="text-2xl font-black tracking-[-0.05em] text-slate-900">Items</h2>
        <div className="mt-4 space-y-3">
          {order.items?.map((item) => (
            <div key={item.id} className="flex items-center justify-between gap-3 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
              <span>{item.name_snapshot} × {item.quantity}</span>
              <strong className="font-bold text-slate-900">₹{item.subtotal}</strong>
            </div>
          ))}
        </div>
        <h2 className="mt-6 text-2xl font-black tracking-[-0.05em] text-slate-900">Total: ₹{order.subtotal}</h2>
        <div className="mt-5">
          <Link to="/orders" className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
            Back to Orders
          </Link>
        </div>
      </div>
    </div>
  );
}