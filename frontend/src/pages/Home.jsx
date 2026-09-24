import { Link } from "react-router-dom";

import { useAuth } from "../context/authContext";

export default function Home() {
  const { user, isAuthenticated } = useAuth();

  const features = [
    { icon: "🚚", title: "Fast delivery", text: "Reliable riders and live order tracking." },
    { icon: "🍔", title: "Local favorites", text: "Explore great restaurants near you." },
    { icon: "💳", title: "Simple checkout", text: "Fast ordering and easy payment confirmation." },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <section className="overflow-hidden rounded-[32px] border border-slate-200/80 bg-white/90 p-6 shadow-[0_28px_80px_rgba(15,23,42,0.08)] md:p-10">
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
          <div className="space-y-6">
            <span className="inline-flex rounded-full border border-brand-200 bg-brand-50 px-3 py-1.5 text-xs font-bold uppercase tracking-[0.12em] text-brand-700">
              Fresh meals, fast delivery
            </span>

            <div className="space-y-4">
              <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900 md:text-5xl lg:text-6xl">
                Food delivered to your door in minutes.
              </h1>
              <p className="max-w-xl text-base text-slate-600 md:text-lg">
                Discover neighbourhood favorites, place your order quickly, and track every step from kitchen to curb with a seamless food delivery experience.
              </p>
            </div>

            {!isAuthenticated ? (
              <div className="flex flex-wrap gap-3">
                <Link to="/restaurants" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
                  Browse Restaurants
                </Link>
                <Link to="/login" className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
                  Login
                </Link>
              </div>
            ) : (
              <div className="flex flex-wrap gap-3">
                {user?.role === "CUSTOMER" && (
                  <>
                    <Link to="/restaurants" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
                      Order Food Now
                    </Link>
                    <Link to="/cart" className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
                      View Cart
                    </Link>
                  </>
                )}

                {user?.role === "RESTAURANT_OWNER" && (
                  <Link to="/restaurant/dashboard" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
                    Open Restaurant Dashboard
                  </Link>
                )}

                {user?.role === "DRIVER" && (
                  <Link to="/driver/dashboard" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
                    Open Driver Dashboard
                  </Link>
                )}
              </div>
            )}
          </div>

          <div className="grid gap-4 sm:grid-cols-3 lg:grid-cols-1">
            {features.map((feature) => (
              <div key={feature.title} className="rounded-[28px] border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-5 shadow-sm">
                <div className="mb-4 grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br from-brand-100 to-brand-200 text-2xl shadow-inner shadow-brand-300/40">
                  {feature.icon}
                </div>
                <h3 className="mb-2 text-xl font-bold text-slate-900">{feature.title}</h3>
                <p className="text-sm leading-6 text-slate-600">{feature.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}