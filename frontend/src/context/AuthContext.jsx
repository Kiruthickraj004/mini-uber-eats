import { createContext, useContext, useState, useEffect } from "react";
import { saveTokens, clearTokens, getAccessToken,} from "../api/authStorage";
import { login, getMe } from "../api/auth";

const AuthContext = createContext(null);
const [user, setUser] = useState(null);

useEffect(() => {
  async function loadUser() {
    if (!accessToken) {
      return;
    }

    try {
      const data = await getMe();

      setUser(data);
    } catch {
      clearTokens();
      setAccessToken(null);
      setUser(null);
    }
  }

  loadUser();
}, [accessToken]);

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(
    getAccessToken()
  );

  async function signIn(username, password) {
    const data = await login(username, password);

    saveTokens(
      data.access,
      data.refresh
    );

    setAccessToken(data.access);
    const currentUser = await getMe();

    setUser(currentUser);

    return currentUser;
  }

  function signOut() {
    clearTokens();
    setAccessToken(null);
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        isAuthenticated: Boolean(accessToken),
        signIn,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}