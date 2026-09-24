import { useEffect, useState } from "react";

import {
  getDriverProfile,
  getAvailableOrders,
  getMyDeliveries,
  claimOrder,
  pickupDelivery,
  completeDelivery,
} from "../api/delivery";

export default function DriverDashboard() {
  const [profile, setProfile] = useState(null);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [error, setError] = useState("");
  const [deliveries, setDeliveries] = useState([]);

  async function loadDashboard() {
    try {
      setError("");
      const [profileData, ordersData, deliveriesData] = await Promise.all([
        getDriverProfile(),
        getAvailableOrders(),
        getMyDeliveries(),
      ]);
      setProfile(profileData);
      setOrders(ordersData);
      setDeliveries(deliveriesData);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  async function handleClaim(orderId) {
    try {
      setActionLoading(orderId);
      setError("");
      await claimOrder(orderId);
      await loadDashboard();
    } catch (error) {
      setError(error.message);
    } finally {
      setActionLoading(null);
    }
  }

  async function handlePickup(deliveryId) {
    try {
      setActionLoading(deliveryId);
      setError("");
      await pickupDelivery(deliveryId);
      await loadDashboard();
    } catch (error) {
      setError(error.message);
    } finally {
      setActionLoading(null);
    }
  }

  async function handleComplete(deliveryId) {
    try {
      setActionLoading(deliveryId);
      setError("");
      await completeDelivery(deliveryId);
      await loadDashboard();
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
          Loading driver dashboard...
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900">Driver Dashboard</h1>
        <p className="mt-2 text-slate-600">Stay on top of deliveries and driver status.</p>
      </div>

      {error && (
        <div className="mb-5 rounded-2xl border border-red-200 bg-red-50 px-3 py-2 text-sm font-medium text-red-700">
          {error}
        </div>
      )}

      {profile && (
        <div className="mb-6 rounded-[28px] border border-slate-200 bg-white p-5 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
          <h2 className="text-2xl font-black tracking-[-0.05em] text-slate-900">Driver Status</h2>
          <div className="mt-4 space-y-2 text-sm text-slate-600">
            <p>Status: {profile.status}</p>
            <p>Vehicle: {profile.vehicle_type || "Not set"}</p>
          </div>
        </div>
      )}

      <div className="space-y-6">
        <div className="rounded-[30px] border border-slate-200 bg-white p-5 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
          <h2 className="text-2xl font-black tracking-[-0.05em] text-slate-900">Available Orders</h2>
          <div className="mt-4 space-y-4">
            {orders.length === 0 ? (
              <div className="rounded-[22px] border border-dashed border-slate-300 bg-slate-50 p-6 text-center text-slate-500">No orders available.</div>
            ) : (
              orders.map((order) => (
                <div key={order.id} className="rounded-[24px] border border-slate-200 bg-slate-50 p-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <h3 className="text-lg font-bold text-slate-900">Order #{order.id}</h3>
                    <span className="inline-flex rounded-full bg-brand-50 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.12em] text-brand-700">
                      {order.status}
                    </span>
                  </div>
                  <div className="mt-3 space-y-2 text-sm text-slate-600">
                    <p>Restaurant: {order.restaurant_name}</p>
                    <p>Total: ₹{order.subtotal}</p>
                  </div>
                  <button
                    type="button"
                    className="mt-4 rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70"
                    disabled={actionLoading === order.id}
                    onClick={() => handleClaim(order.id)}
                  >
                    {actionLoading === order.id ? "Claiming..." : "Claim Order"}
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="rounded-[30px] border border-slate-200 bg-white p-5 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
          <h2 className="text-2xl font-black tracking-[-0.05em] text-slate-900">My Deliveries</h2>
          <div className="mt-4 space-y-4">
            {deliveries.length === 0 ? (
              <div className="rounded-[22px] border border-dashed border-slate-300 bg-slate-50 p-6 text-center text-slate-500">No deliveries yet.</div>
            ) : (
              deliveries.map((delivery) => (
                <div key={delivery.id} className="rounded-[24px] border border-slate-200 bg-slate-50 p-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <h3 className="text-lg font-bold text-slate-900">Delivery #{delivery.id}</h3>
                    <span className="inline-flex rounded-full bg-brand-50 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.12em] text-brand-700">
                      {delivery.status}
                    </span>
                  </div>
                  <p className="mt-3 text-sm text-slate-600">Order #{delivery.order}</p>

                  {delivery.status === "ASSIGNED" && (
                    <button
                      type="button"
                      className="mt-4 rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70"
                      disabled={actionLoading === delivery.id}
                      onClick={() => handlePickup(delivery.id)}
                    >
                      {actionLoading === delivery.id ? "Processing..." : "Pickup Order"}
                    </button>
                  )}

                  {delivery.status === "PICKED_UP" && (
                    <button
                      type="button"
                      className="mt-4 rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70"
                      disabled={actionLoading === delivery.id}
                      onClick={() => handleComplete(delivery.id)}
                    >
                      {actionLoading === delivery.id ? "Completing..." : "Complete Delivery"}
                    </button>
                  )}

                  {delivery.status === "DELIVERED" && (
                    <div className="mt-4 rounded-2xl border border-brand-200 bg-brand-50 px-3 py-2 text-sm font-medium text-brand-800">
                      ✓ Delivery completed
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}