import { Link } from "react-router-dom";

import { useAuth } from "../context/authContext";

export default function Home() {
  const { user, isAuthenticated } = useAuth();

  const features = [
    { icon: "🚚", title: "Fast delivery", text: "Reliable riders and live order tracking across the city." },
    { icon: "🍔", title: "Local favorites", text: "Explore trending restaurants and chef-curated daily picks." },
    { icon: "💳", title: "Simple checkout", text: "Quick ordering, smooth payments, and real-time confirmation." },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <section className="overflow-hidden rounded-[34px] border border-brand-100 bg-white/90 p-6 shadow-[0_30px_90px_rgba(90,36,18,0.08)] md:p-10">
        <div className="grid gap-8 lg:grid-cols-[1.25fr_0.75fr] lg:items-center">
          <div className="space-y-6">
            <span className="inline-flex rounded-full border border-brand-200 bg-brand-50 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-brand-700">
              Fresh meals, fast delivery
            </span>

            <div className="space-y-4">
              <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900 md:text-5xl lg:text-6xl">
                Craving something great?<br />
                We bring it to you fast.
              </h1>
              <p className="max-w-xl text-base text-slate-600 md:text-lg">
                Discover neighborhood favorites, build your perfect order, and track every step from kitchen prep to doorstep delivery.
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
                    <Link to="/cart" className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition hover:border-brand-200 hover:bg-brand-50 hover:text-brand-700">
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
              <div key={feature.title} className="rounded-[28px] border border-brand-100 bg-gradient-to-br from-brand-50 via-white to-white p-5 shadow-[0_20px_40px_rgba(76,31,14,0.05)]">
                <div className="mb-4 grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br from-brand-100 to-brand-200 text-2xl shadow-inner shadow-brand-300/50">
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