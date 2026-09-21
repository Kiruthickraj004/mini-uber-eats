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

  async function handleQuantityChange(
    itemId,
    quantity
  ) {
    try {
      const updatedCartItem =
        await updateCartItem(
          itemId,
          quantity
        );

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
    return <p>Loading cart...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div>
        <h1>Your Cart</h1>
        <p>Your cart is empty.</p>

        <Link to="/restaurants">
          Browse Restaurants
        </Link>
      </div>
    );
  }

  return (
    <div>
      <h1>Your Cart</h1>

      <h2>{cart.restaurant_name}</h2>

      {cart.items.map((item) => (
        <div key={item.id}>
          <h3>{item.menu_item_name}</h3>

          <p>
            ₹{item.unit_price}
          </p>

          <p>
            Quantity: {item.quantity}
          </p>

          <button
            onClick={() =>
              handleQuantityChange(
                item.id,
                item.quantity - 1
              )
            }
            disabled={item.quantity <= 1}
          >
            -
          </button>

          <button
            onClick={() =>
              handleQuantityChange(
                item.id,
                item.quantity + 1
              )
            }
          >
            +
          </button>

          <button
            onClick={() =>
              handleRemove(item.id)
            }
          >
            Remove
          </button>
        </div>
      ))}

      <hr />

      <h2>
        Subtotal: ₹{cart.subtotal}
      </h2>

      <button
        onClick={handleClearCart}
      >
        Clear Cart
      </button>

      <br />

      <Link to="/checkout">
        Proceed to Checkout
      </Link>
    </div>
  );
}