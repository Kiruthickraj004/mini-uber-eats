import {BrowserRouter,Routes,Route,} from "react-router-dom";
import Navbar from "./components/Navbar";
import RoleRoute from "./components/RoleRoute";
import Login from "./pages/Login";
import Restaurants from "./pages/Restaurant";
import RestaurantMenu from "./pages/RestaurantMenu";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import OrderDetails from "./pages/OrderDetails";
import RestaurantDashboard from "./pages/RestaurantDashboard";
import DriverDashboard from "./pages/DriverDashboard";


function Home() {
  return <h1>Mini Uber Eats</h1>;
}

export default function App() {
  return (
    <>
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />

          {/* Login */}
          <Route path="/login" element={<Login />} />

          {/* Restaurant and menus */}
          <Route path="/restaurants" element={<Restaurants />} />
          <Route path="/restaurants/:restaurantId" element={<RestaurantMenu />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/orders" element={<Orders />} />
            <Route path="/orders/:orderId" element={<OrderDetails />}/>
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route
              element={
                <RoleRoute
                  allowedRoles={["RESTAURANT_OWNER"]}
                />
              }
            >
              <Route
                path="/restaurant/dashboard"
                element={<RestaurantDashboard />}
              />
            </Route>

            <Route
              element={
                <RoleRoute
                  allowedRoles={["DRIVER"]}
                />
              }
            >
              <Route
                path="/driver/dashboard"
                element={<DriverDashboard />}
              />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}