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

   const refreshToken = (token) => {
      console.log(token)
      localStorage.setItem('refreshToken', token)
   }

   const removeToken = () => {
      localStorage.removeItem('authToken');
   }

   const setExpirationTime = (time) => {
      localStorage.setItem('expirationTime', time * 1000)
   }

   const setExpirationTimeRefresh = (time) => {
      localStorage.setItem('refreshExpirationTime', time * 1000)
   }

   const setStartTime = (time) => {
      localStorage.setItem('startTime', time)
   }

   const setCurrentTime = (time) => {
      localStorage.setItem('currentTime', time)
   }


   // Function to check if the user is already authenticated or not
   const authenticateUser = async () => {

      const storedToken = localStorage.getItem('authToken');
      const refreshToken = localStorage.getItem('refreshToken')
      const expirationTime = localStorage.getItem('expirationTime');
      const refreshTime = localStorage.getItem('refreshExpirationTime')

      const startTime = localStorage.getItem('startTime')

      const currentTime = localStorage.getItem('currentTime')

      console.log(startTime)
      console.log(expirationTime)
      console.log(refreshTime)



      if ((currentTime - startTime) > expirationTime) {
         ///GET NEW REFRESH TOKEN

         if ((currentTime -startTime) > refreshTime){
            logOutUser()
         } else{

            

         }

      } else
      if (storedToken) {
         //try {
         //const response = await axios.post(`, { headers: { Authorization: `Bearer ${storedToken}` } });
         setIsLoggedIn(true);
         setLoading(false);

         //} catch (error) {
         // setIsLoggedIn(false);
         //setLoading(false);
         //setUser(null);
         // }
      } else {
         setIsLoggedIn(false);
         setLoading(false);

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
      <AuthContext.Provider value={{ user, isLoggedIn, setExpirationTime, setExpirationTimeRefresh, storeToken, refreshToken, authenticateUser, setStartTime, setCurrentTime, logOutUser }}>
         {props.children}
      </AuthContext.Provider>
   )
}

export { AuthProviderWrapper, AuthContext };