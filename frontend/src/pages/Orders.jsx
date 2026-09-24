import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getOrders } from "../api/orders";

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadOrders() {
      try {
        const data = await getOrders();
        setOrders(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadOrders();
  }, []);

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
          Loading orders...
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

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900">My Orders</h1>
        <p className="mt-2 text-slate-600">Track your latest orders.</p>
      </div>

      {orders.length === 0 ? (
        <div className="rounded-[30px] border border-dashed border-slate-300 bg-white/80 p-8 text-center shadow-[0_18px_40px_rgba(15,23,42,0.04)]">
          <p className="text-slate-600">You haven’t placed any orders yet.</p>
          <div className="mt-5">
            <Link to="/restaurants" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
              Browse Restaurants
            </Link>
          </div>
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
                <p>Restaurant: {order.restaurant_name}</p>
                <p>Total: ₹{order.subtotal}</p>
                <p>Payment Status: {order.payment?.status}</p>
              </div>
              <Link to={`/orders/${order.id}`} className="mt-5 inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
                View Order
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}