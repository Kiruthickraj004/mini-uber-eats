import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/authContext";

export default function Navbar() {
  const { user, isAuthenticated, signOut } = useAuth();
  const navigate = useNavigate();

  return (
    <nav className="sticky top-0 z-40 border-b border-brand-100/80 bg-white/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 md:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3 text-lg font-extrabold tracking-[-0.04em] text-slate-900">
          <span className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-brand-500 via-brand-400 to-brand-300 text-lg text-white shadow-lg shadow-brand-500/25">
            U
          </span>
          <span>Mini Uber Eats</span>
        </Link>

        <div className="hidden items-center gap-2 md:flex">
          <Link to="/restaurants" className="rounded-full px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-brand-50 hover:text-brand-700">
            Restaurants
          </Link>

          {isAuthenticated && (
            <>
              <Link to="/cart" className="rounded-full px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-brand-50 hover:text-brand-700">
                Cart
              </Link>
              <Link to="/orders" className="rounded-full px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-brand-50 hover:text-brand-700">
                My Orders
              </Link>
            </>
          )}

          {user?.role === "RESTAURANT_OWNER" && (
            <Link to="/restaurant/dashboard" className="rounded-full px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-brand-50 hover:text-brand-700">
              Restaurant Dashboard
            </Link>
          )}

          {user?.role === "DRIVER" && (
            <Link to="/driver/dashboard" className="rounded-full px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-brand-50 hover:text-brand-700">
              Driver Dashboard
            </Link>
          )}
        </div>

        {isAuthenticated ? (
          <div className="flex items-center gap-3">
            <span className="hidden rounded-full border border-brand-200 bg-brand-50 px-3 py-1.5 text-xs font-semibold text-brand-800 sm:inline-flex">
              {user?.email}
            </span>
            <button
              type="button"
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-brand-200 hover:bg-brand-50 hover:text-brand-700"
              onClick={() => {
                signOut();
                navigate("/login");
              }}
            >
              Logout
            </button>
          </div>
        ) : (
          <Link to="/login" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}