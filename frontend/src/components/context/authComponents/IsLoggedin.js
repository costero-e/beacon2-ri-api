import { useContext } from "react";
import { AuthContext } from "../AuthContext";
import { Navigate } from "react-router-dom";

function IsLoggedin({ children }) {

   const { isLoggedIn, isLoading } = useContext(AuthContext);

   // If the authentication is still loading
   if (isLoading) return <p>Loading ...</p>;

   if (!isLoggedIn) {
      // If the user is logged in
      return <Navigate to="/home" />;
   } else {
      // If the user is logged in, allow to see the page
      return children;
   }
}

export default IsLoggedin;
