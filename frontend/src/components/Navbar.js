import { NavLink } from 'react-router-dom';
import './Navbar.scss'
import React, { useState } from 'react';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import SignInForm from './SignInForm';


function Navbar() {

    const [selected, setIsSelected ] = useState('')

    const { isLoggedIn, user, logOutUser } = useContext(AuthContext);

    const logOut = (e) => {

        logOutUser()

    } 
     
    return (

        
    
            <nav id="nav">
                <div className="nav left">
                   
                        <span className="gradient skew"><h1 className="logo un-skew"><a href="/">
                        < img src="./home2.png" className="homeIcon" alt="home" />
                    </a></h1></span>

                </div>
                <div class="nav right">
                    {!isLoggedIn && <NavLink to= "/sign-up"  className= {selected ? 'nav-link': 'nav-link'} onClick={() => { setIsSelected(true)}}><span className="nav-link-span"><span className="u-nav">Sign Up</span></span> </NavLink>}
                    {!isLoggedIn && <NavLink to ="/sign-in" className={selected ? 'nav-link': 'nav-link'} onClick={() => { setIsSelected(true)}}> <span className="nav-link-span"><span className="u-nav">Sign In</span></span></NavLink>}
                    <NavLink to="/members" className={selected ? 'nav-link': 'nav-link'} onClick={() => { setIsSelected(true)}}><span className="nav-link-span"><span className="u-nav">Network members</span></span></NavLink>
                    {isLoggedIn && <NavLink to= "/sign-in" className= {selected ? 'nav-link': 'nav-link'} onClick={logOut}><span className="nav-link-span"><span className="u-nav">LOG OUT</span></span> </NavLink>}
                </div>
            </nav>
        


    )
}


export default Navbar;