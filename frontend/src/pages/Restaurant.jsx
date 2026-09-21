import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getRestaurants } from "../api/restaurants";

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
    return <p>Loading restaurants...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h1>Restaurants</h1>

      {restaurants.map((restaurant) => (
        <div key={restaurant.id}>
          <h2>{restaurant.name}</h2>

          <p>{restaurant.description}</p>

          <p>
            {restaurant.address}
          </p>

          <p>
            Status: {restaurant.status}
          </p>

          <Link
            to={`/restaurants/${restaurant.id}`}
          >
            View Menu
          </Link>
        </div>
      ))}
    </div>
  );
}