import { Link } from "react-router-dom";

import { useAuth } from "../context/authContext";

export default function Home() {
  const { user, isAuthenticated } = useAuth();

  return (
    <div>
      <h1>Mini Uber Eats</h1>

      <p>
        A food ordering and delivery platform
        built with React, Django REST Framework,
        PostgreSQL, Redis and Celery.
      </p>

      {!isAuthenticated && (
        <div>
          <Link to="/restaurants">
            Browse Restaurants
          </Link>

          {" | "}

          <Link to="/login">
            Login
          </Link>
        </div>
      )}

      {user?.role === "CUSTOMER" && (
        <div>
          <h2>Customer</h2>

          <Link to="/restaurants">
            Browse Restaurants
          </Link>

          {" | "}

          <Link to="/cart">
            View Cart
          </Link>

          {" | "}

          <Link to="/orders">
            My Orders
          </Link>
        </div>
      )}

      {user?.role === "RESTAURANT_OWNER" && (
        <div>
          <h2>Restaurant Owner</h2>

          <Link to="/restaurant/dashboard">
            Open Restaurant Dashboard
          </Link>
        </div>
      )}

      {user?.role === "DRIVER" && (
        <div>
          <h2>Driver</h2>

          <Link to="/driver/dashboard">
            Open Driver Dashboard
          </Link>
        </div>
      )}
    </div>
  );
}