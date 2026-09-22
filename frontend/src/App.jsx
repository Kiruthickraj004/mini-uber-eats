import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/protectedRoutes";
import RoleRoute from "./components/RoleRoute";
import Home from "./pages/Home";
import Register from "./pages/Register"
import Login from "./pages/Login";
import Restaurants from "./pages/Restaurant";
import RestaurantMenu from "./pages/RestaurantMenu";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Orders from "./pages/Orders";
import OrderDetails from "./pages/OrderDetails";
import RestaurantDashboard from "./pages/RestaurantDashboard";
import DriverDashboard from "./pages/DriverDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        <Route path="/restaurants" element={<Restaurants />} />
        <Route path="/restaurants/:restaurantId" element={<RestaurantMenu />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/orders" element={<Orders />} />
          <Route path="/orders/:orderId" element={<OrderDetails />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout" element={<Checkout />} />

          <Route
            element={<RoleRoute allowedRoles={["RESTAURANT_OWNER"]} />}
          >
            <Route
              path="/restaurant/dashboard"
              element={<RestaurantDashboard />}
            />
          </Route>

          <Route element={<RoleRoute allowedRoles={["DRIVER"]} />}>
            <Route path="/driver/dashboard" element={<DriverDashboard />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}