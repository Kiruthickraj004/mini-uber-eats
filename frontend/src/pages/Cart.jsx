import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  getCart,
  updateCartItem,
  removeCartItem,
  clearCart,
} from "../api/cart";

export default function Cart() {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const cartItems = Array.isArray(cart?.items) ? cart.items : [];

  async function loadCart() {
    try {
      const data = await getCart();
      setCart(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCart();
  }, []);

  async function handleQuantityChange(itemId, quantity) {
    try {
      await updateCartItem(itemId, quantity);
      await loadCart();
    } catch (error) {
      setError(error.message);
    }
  }

  async function handleRemove(itemId) {
    try {
      await removeCartItem(itemId);
      await loadCart();
    } catch (error) {
      setError(error.message);
    }
  }

  async function handleClearCart() {
    try {
      await clearCart();
      await loadCart();
    } catch (error) {
      setError(error.message);
    }
  }

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="rounded-[28px] border border-dashed border-slate-300 bg-white/80 p-10 text-center text-slate-500">
          Loading cart...
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

  if (!cart || cartItems.length === 0) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 md:px-6 lg:px-8">
        <div className="mx-auto max-w-lg rounded-[30px] border border-slate-200 bg-white p-8 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
          <h1 className="text-3xl font-black tracking-[-0.08em] text-slate-900">Your Cart</h1>
          <p className="mt-3 text-slate-600">Your cart is empty.</p>
          <div className="mt-6">
            <Link to="/restaurants" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
              Browse Restaurants
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-4xl font-black tracking-[-0.08em] text-slate-900">Your Cart</h1>
        <p className="mt-2 text-slate-600">{cart.restaurant_name}</p>
      </div>

      <div className="space-y-4">
        {cartItems.map((item) => (
          <div key={item.id} className="rounded-[28px] border border-slate-200 bg-white p-5 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h3 className="text-xl font-bold text-slate-900">{item.menu_item_name}</h3>
                <p className="mt-1 text-sm text-slate-600">Quantity: {item.quantity}</p>
              </div>
              <strong className="text-lg font-bold text-slate-900">₹{item.unit_price}</strong>
            </div>

            <div className="mt-4 flex flex-wrap items-center gap-3">
              <button
                type="button"
                className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
                onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                disabled={item.quantity <= 1}
              >
                -
              </button>
              <button
                type="button"
                className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
                onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
              >
                +
              </button>
              <button
                type="button"
                className="rounded-full bg-brand-50 px-4 py-2 text-sm font-semibold text-brand-700 transition hover:bg-brand-100"
                onClick={() => handleRemove(item.id)}
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 rounded-[30px] border border-slate-200 bg-white p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)]">
        <h2 className="text-2xl font-black tracking-[-0.05em] text-slate-900">Subtotal: ₹{cart.subtotal}</h2>
        <div className="mt-5 flex flex-wrap items-center gap-3">
          <button type="button" className="rounded-full border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" onClick={handleClearCart}>Clear Cart</button>
          <Link to="/checkout" className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition hover:-translate-y-0.5 hover:shadow-brand-500/35">
            Proceed to Checkout
          </Link>
        </div>
      </div>
    </div>
  );
}