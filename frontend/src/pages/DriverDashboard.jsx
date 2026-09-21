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
  const [actionLoading, setActionLoading] =
    useState(null);
  const [error, setError] = useState("");
  const [deliveries, setDeliveries] = useState([]);
  async function loadDashboard() {
    try {
     setError("");

      const [ profileData,ordersData,deliveriesData,] = await Promise.all([getDriverProfile(),getAvailableOrders(),getMyDeliveries(),]);
      setProfile(profileData);
      setOrders(ordersData);
      setDeliveries(deliveriesData);
    }catch (error) {
      setError(error.message);
    }finally {
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
    return <p>Loading driver dashboard...</p>;
  }

  return (
    <div>
      <h1>Driver Dashboard</h1>

      {error && <p>{error}</p>}

      {profile && (
        <div>
          <h2>Driver Status</h2>

          <p>
            Status: {profile.status}
          </p>

          <p>
            Vehicle: {profile.vehicle_type}
          </p>
        </div>
      )}

      <hr />

      <h2>Available Orders</h2>

      {orders.length === 0 ? (
        <p>No orders available.</p>
      ) : (
        orders.map((order) => (
          <div key={order.id}>
            <h3>
              Order #{order.id}
            </h3>

            <p>
              Restaurant:{" "}
              {order.restaurant_name}
            </p>

            <p>
              Total: ₹{order.subtotal}
            </p>

            <p>
              Status: {order.status}
            </p>

            <button
              disabled={
                actionLoading === order.id
              }
              onClick={() =>
                handleClaim(order.id)
              }
            >
              {actionLoading === order.id
                ? "Claiming..."
                : "Claim Order"}
            </button>

            <hr />
          </div>
        ))
      )}

      <hr />

      <h2>My Deliveries</h2>

      {deliveries.length === 0 ? (
        <p>No deliveries yet.</p>
      ) : (
        deliveries.map((delivery) => (
          <div key={delivery.id}>
            <h3>
              Delivery #{delivery.id}
            </h3>

            <p>
              Order #{delivery.order}
            </p>

            <p>
              Status: {delivery.status}
            </p>

            {delivery.status === "ASSIGNED" && (
              <button
                disabled={
                  actionLoading === delivery.id
                }
                onClick={() =>
                  handlePickup(delivery.id)
                }
              >
                {actionLoading === delivery.id
                  ? "Processing..."
                  : "Pickup Order"}
              </button>
            )}

            {delivery.status === "PICKED_UP" && (
              <button
                disabled={
                  actionLoading === delivery.id
                }
                onClick={() =>
                  handleComplete(delivery.id)
                }
              >
                {actionLoading === delivery.id
                  ? "Completing..."
                  : "Complete Delivery"}
              </button>
            )}

            {delivery.status === "DELIVERED" && (
              <p>✓ Delivery completed</p>
            )}

            <hr />
          </div>
        ))
      )}

    </div>
  );
}