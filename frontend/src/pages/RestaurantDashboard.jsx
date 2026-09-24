import { useEffect, useState } from "react";

import {
  getRestaurantOrders,
  acceptOrder,
  rejectOrder,
  startPreparing,
  markOrderReady,
} from "../api/orders";

export default function RestaurantDashboard() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [error, setError] = useState("");

  async function loadOrders() {
    try {
      setError("");
      const data = await getRestaurantOrders();
      setOrders(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadOrders();
  }, []);

  async function performAction(orderId, action) {
    try {
      setActionLoading(orderId);
      setError("");
      await action(orderId);
      await loadOrders();
    } catch (error) {
      setError(error.message);
    } finally {
      setActionLoading(null);
    }
  }

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
          Loading restaurant orders...
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900">Restaurant Dashboard</h1>
        <p className="mt-2 text-slate-600">Manage incoming customer orders.</p>
      </div>

      {error && (
        <div className="mb-5 rounded-2xl border border-red-200 bg-red-50 px-3 py-2 text-sm font-medium text-red-700">
          {error}
        </div>
      )}

      {orders.length === 0 ? (
        <div className="rounded-[30px] border border-dashed border-slate-300 bg-white/80 p-8 text-center text-slate-500 shadow-[0_18px_40px_rgba(15,23,42,0.04)]">
          No orders yet.
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div key={order.id} className="rounded-[28px] border border-slate-200 bg-white p-5 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <h3 className="text-xl font-bold text-slate-900">Order #{order.id}</h3>
                <span className="inline-flex rounded-full bg-brand-50 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.12em] text-brand-700">
                  {order.status}
                </span>
              </div>
              <div className="mt-4 space-y-2 text-sm text-slate-600">
                <p>Customer: {order.customer_email}</p>
                <p>Total: ₹{order.subtotal}</p>
              </div>

              {order.status === "PENDING" && (
                <div className="mt-5 flex flex-wrap gap-3">
                  <button className="rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70" disabled={actionLoading === order.id} onClick={() => performAction(order.id, acceptOrder)}>
                    {actionLoading === order.id ? "Accepting..." : "Accept"}
                  </button>
                  <button className="rounded-full border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-70" disabled={actionLoading === order.id} onClick={() => performAction(order.id, rejectOrder)}>
                    {actionLoading === order.id ? "Rejecting..." : "Reject"}
                  </button>
                </div>
              )}

              {order.status === "CONFIRMED" && (
                <button className="mt-5 rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70" disabled={actionLoading === order.id} onClick={() => performAction(order.id, startPreparing)}>
                  {actionLoading === order.id ? "Starting..." : "Start Preparing"}
                </button>
              )}

              {order.status === "PREPARING" && (
                <button className="mt-5 rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70" disabled={actionLoading === order.id} onClick={() => performAction(order.id, markOrderReady)}>
                  {actionLoading === order.id ? "Updating..." : "Mark Ready"}
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}