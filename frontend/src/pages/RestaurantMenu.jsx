import { useEffect, useState } from "react";
import {
  Link,
  useParams,
} from "react-router-dom";

import { getRestaurantMenu } from "../api/menu";
import { addToCart } from "../api/cart";

export default function RestaurantMenu() {
  const { restaurantId } = useParams();

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [addingItemId, setAddingItemId] =
  useState(null);

  const [cartMessage, setCartMessage] =
  useState("");

  useEffect(() => {
    async function loadMenu() {
      try {
        const data = await getRestaurantMenu(
          restaurantId
        );

        setItems(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadMenu();
  }, [restaurantId]);

  if (loading) {
    return <p>Loading menu...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  async function handleAddToCart(itemId) {
  setAddingItemId(itemId);
  setCartMessage("");

  try {
    await addToCart(itemId);

    setCartMessage(
      "Item added to cart."
    );
  } catch (error) {
    setCartMessage(error.message);
  } finally {
    setAddingItemId(null);
  }
}

  return (
    <div>
      <Link to="/restaurants">
        ← Restaurants
      </Link>

      <h1>Menu</h1>

      {items.length === 0 ? (
        <p>No menu items available.</p>
      ) : (
        items.map((item) => (
          <div key={item.id}>
            <h2>{item.name}</h2>

            <p>{item.description}</p>

            <p>
              ₹{item.price}
            </p>

            <button onClick={() => handleAddToCart(item.id)} disabled={addingItemId === item.id}>
              {addingItemId === item.id ? "Adding..." : "Add to Cart"} 
            </button>
          </div>
        ))
      )}
    </div>
  );
}