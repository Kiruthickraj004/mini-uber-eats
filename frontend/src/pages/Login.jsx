import { useState } from "react";
import { Link,useLocation,useNavigate } from "react-router-dom";

import { useAuth } from "../context/authContext";

export default function Login() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const registrationMessage = location.state?.message;
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const user = await signIn(username, password);

      if (user?.role === "RESTAURANT_OWNER") {
        navigate("/restaurant/dashboard");
      } else if (user?.role === "DRIVER") {
        navigate("/driver/dashboard");
      } else {
        navigate("/");
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Login</h1>
      {registrationMessage && <p>{registrationMessage}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Username
          </label>

          <input
            type="text"
            value={username}
            onChange={(event) =>
              setUsername(event.target.value)
            }
            required
          />
        </div>

        <div>
          <label>
            Password
          </label>

          <input
            type="password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />
        </div>

        {error && (
          <p>{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
      <p>Don't have an account?{" "}<Link to="/register">Create an account</Link></p>
    </div>
  );
}