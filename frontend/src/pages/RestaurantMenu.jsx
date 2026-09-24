import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getRestaurantMenu } from "../api/menu";
import { addToCart } from "../api/cart";

export default function RestaurantMenu() {
  const { restaurantId } = useParams();

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [addingItemId, setAddingItemId] = useState(null);
  const [cartMessage, setCartMessage] = useState("");

  useEffect(() => {
    async function loadMenu() {
      try {
        const data = await getRestaurantMenu(restaurantId);
        setItems(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadMenu();
  }, [restaurantId]);

  async function handleAddToCart(itemId) {
    setAddingItemId(itemId);
    setCartMessage("");

    try {
      await addToCart(itemId);
      setCartMessage("Item added to cart.");
    } catch (error) {
      setCartMessage(error.message);
    } finally {
      setAddingItemId(null);
    }
  }

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
          Loading menu...
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
      <div className="mb-6">
        <Link to="/restaurants" className="inline-flex items-center rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
          ← Restaurants
        </Link>
        <h1 className="mt-5 text-4xl font-black tracking-[-0.08em] text-slate-900">Menu</h1>
      </div>

      {cartMessage && (
        <div className="mb-5 rounded-2xl border border-brand-200 bg-brand-50 px-3 py-2 text-sm font-medium text-brand-800">
          {cartMessage}
        </div>
      )}

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {items.length === 0 ? (
          <div className="col-span-full rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
            No menu items available.
          </div>
        ) : (
          items.map((item) => (
            <div key={item.id} className="rounded-[28px] border border-slate-200 bg-white p-5 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
              <h3 className="text-xl font-bold text-slate-900">{item.name}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">{item.description}</p>
              <div className="mt-4 flex items-center justify-between text-sm text-slate-600">
                <span>Price</span>
                <strong className="text-lg font-bold text-slate-900">₹{item.price}</strong>
              </div>
              <button
                className="mt-5 w-full rounded-2xl bg-gradient-to-r from-brand-500 to-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35 disabled:cursor-not-allowed disabled:opacity-70"
                onClick={() => handleAddToCart(item.id)}
                disabled={addingItemId === item.id}
              >
                {addingItemId === item.id ? "Adding..." : "Add to Cart"}
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}