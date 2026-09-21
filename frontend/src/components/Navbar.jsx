import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/authContext";

export default function Navbar() {
  const {
    user,
    isAuthenticated,
    signOut,
  } = useAuth();
  const navigate = useNavigate();
  return (
    <nav>
      <Link to="/">
        Mini Uber Eats
      </Link>

      {" | "}

      <Link to="/restaurants">
        Restaurants
      </Link>

      {isAuthenticated && (
        <>
          {" | "}

          <Link to="/cart">
            Cart
          </Link>

          {" | "}

          <Link to="/orders">
            My Orders
          </Link>
        </>
      )}

      {user?.role === "RESTAURANT_OWNER" && (
        <>
          {" | "}

          <Link to="/restaurant/dashboard">
            Restaurant Dashboard
          </Link>
        </>
      )}

      {user?.role === "DRIVER" && (
        <>
          {" | "}

          <Link to="/driver/dashboard">
            Driver Dashboard
          </Link>
        </>
      )}

      <span>
        {" | "}
      </span>

      {isAuthenticated ? (
        <>
          <span>
            {user?.email}
          </span>

          {" "}

          <button onClick={() =>{signOut(); navigate("/login");}}>
            Logout
          </button>
        </>
      ) : (
        <Link to="/login">
          Login
        </Link>
      )}
    </nav>
  );
}