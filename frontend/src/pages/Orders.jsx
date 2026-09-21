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
    return <p>Loading orders...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h1>My Orders</h1>

      {orders.length === 0 ? (
        <div>
          <p>You haven't placed any orders yet.</p>

          <Link to="/restaurants">
            Browse Restaurants
          </Link>
        </div>
      ) : (
        orders.map((order) => (
          <div key={order.id}>
            <h2>Order #{order.id}</h2>

            <p>
              Restaurant: {order.restaurant_name}
            </p>

            <p>
              Total: ₹{order.subtotal}
            </p>

            <p>
              Order Status: {order.status}
            </p>

            <p>
              Payment Status:{" "}
              {order.payment?.status}
            </p>

            <Link to={`/orders/${order.id}`}>
              View Order
            </Link>

            <hr />
          </div>
        ))
      )}
    </div>
  );
}