import React, { createContext, useState, useEffect, useContext } from 'react';
import { getAuthStatus, loginUser as apiLogin, logoutUser as apiLogout } from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // On initial load, check the user's authentication status from the backend.
    // This handles cases where the user is already logged in (e.g., session cookie).
    const checkLoggedIn = async () => {
      try {
        const { data } = await getAuthStatus();
        if (data.logged_in) {
          setUser(data.user);
        }
      } catch (error) {
        // This is expected if the user is not logged in.
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkLoggedIn();
  }, []);

  const login = async (username, password) => {
    // This login function is a wrapper around the API call
    // that also updates the global user state.
    try {
      const { data } = await apiLogin(username, password);
      setUser(data.user);
      return data;
    } catch (error) {
      setUser(null);
      throw error;
    }
  };

  const logout = async () => {
    // The logout function clears the user state after calling the API.
    try {
      await apiLogout();
      setUser(null);
    } catch (error) {
      console.error("Logout failed, but clearing session locally.", error);
      setUser(null);
    }
  };

  const value = {
    user,
    loading,
    login,
    logout,
  };

  // We don't render the rest of the app until we've checked for a logged-in user.
  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
