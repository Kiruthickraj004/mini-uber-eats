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
    return <p>Loading restaurant orders...</p>;
  }

  return (
    <div>
      <h1>Restaurant Dashboard</h1>

      {error && <p>{error}</p>}

      {orders.length === 0 ? (
        <p>No orders yet.</p>
      ) : (
        orders.map((order) => (
          <div key={order.id}>
            <h2>Order #{order.id}</h2>

            <p>
              Customer: {order.customer_email}
            </p>

            <p>
              Total: ₹{order.subtotal}
            </p>

            <p>
              Status: {order.status}
            </p>

            {order.status === "PENDING" && (
              <>
                <button
                  disabled={actionLoading === order.id}
                  onClick={() =>
                    performAction(
                      order.id,
                      acceptOrder
                    )
                  }
                >
                  Accept
                </button>

                <button
                  disabled={actionLoading === order.id}
                  onClick={() =>
                    performAction(
                      order.id,
                      rejectOrder
                    )
                  }
                >
                  Reject
                </button>
              </>
            )}

            {order.status === "CONFIRMED" && (
              <button
                disabled={actionLoading === order.id}
                onClick={() =>
                  performAction(
                    order.id,
                    startPreparing
                  )
                }
              >
                Start Preparing
              </button>
            )}

            {order.status === "PREPARING" && (
              <button
                disabled={actionLoading === order.id}
                onClick={() =>
                  performAction(
                    order.id,
                    markOrderReady
                  )
                }
              >
                Mark Ready
              </button>
            )}

            <hr />
          </div>
        ))
      )}
    </div>
  );
}