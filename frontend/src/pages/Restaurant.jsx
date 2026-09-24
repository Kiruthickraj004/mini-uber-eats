import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getRestaurants } from "../api/restaurant";

export default function Restaurants() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRestaurants() {
      try {
        const data = await getRestaurants();
        setRestaurants(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadRestaurants();
  }, []);

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
          Loading restaurants...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <div className="mb-8 flex items-end justify-between gap-3">
        <div>
          <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900">Restaurants</h1>
          <p className="mt-2 text-slate-600">Fresh picks from your neighborhood.</p>
        </div>
      </div>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {restaurants.map((restaurant) => (
          <div key={restaurant.id} className="rounded-[28px] border border-slate-200 bg-white p-5 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
            <div className="mb-4 flex items-center justify-between gap-3">
              <span className="inline-flex rounded-full bg-brand-50 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.12em] text-brand-700">
                {restaurant.status}
              </span>
            </div>
            <h3 className="text-xl font-bold text-slate-900">{restaurant.name}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">{restaurant.description}</p>
            <p className="mt-3 text-sm text-slate-500">{restaurant.address}</p>

            <Link
              to={`/restaurants/${restaurant.id}`}
              className="mt-5 inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-r from-brand-500 to-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35"
            >
              View Menu
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}