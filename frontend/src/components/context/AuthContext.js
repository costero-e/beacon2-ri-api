import React, { useState, createContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

function AuthProviderWrapper(props) {
   
   // Store the variables we want to share
   const [user, setUser] = useState(null);
   const [isLoggedIn, setIsLoggedIn] = useState(false);
   const [isLoading, setLoading] = useState(true);

   // Functions to store and delete the token received by the backend in the browser
   const storeToken = (token) => {
      localStorage.setItem('authToken', token);
   }

   const removeToken = () => {
      localStorage.removeItem('authToken');
   }
   
   // Function to check if the user is already authenticated or not
   const authenticateUser = async () => {
      setLoading(true);
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
         try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/auth/verify`, { headers: { Authorization: `Bearer ${storedToken}` } });
            setIsLoggedIn(true);
            setLoading(false);
            setUser(response.data);
         } catch (error) {
            setIsLoggedIn(false);
            setLoading(false);
            setUser(null);
         }
      } else {
         setIsLoggedIn(false);
         setLoading(false);
         setUser(null);
      }
   };

   const logOutUser = () => {
      removeToken();
      authenticateUser();
   }

   useEffect(() => {
      authenticateUser();
   }, []);

   return (
      <AuthContext.Provider value={{ user, isLoggedIn, isLoading, storeToken, authenticateUser, logOutUser }}>
         {props.children}
      </AuthContext.Provider>
   )
}

export { AuthProviderWrapper, AuthContext };