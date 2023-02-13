import { NavLink } from 'react-router-dom';
import './Navbar.css'
import React, { useState } from 'react';

function Navbar() {
    const [isActive, setActive] = useState('');
    const [activeHome, setActiveHome] = useState(true)
    const [open, setOpen] = useState(false)

 

    return (
        <div className="navBar">
            <NavLink onClick={() => { setActiveHome(false); setOpen(!open); setActive(true)}} className={isActive ? 'selectedLogin' : 'login'}>Login</NavLink>
           
            {open && <div className={`dropdown-menu ${open ? 'active2' : 'inactive'}`}>
                <ul className="userMenu">
                    <NavLink to="/sign-up" onClick={() => { setOpen(!open) }} className="positionLink" ><img className="userIcon" src="/add-user.png" alt="addUser" />Sign up</NavLink>
                     <NavLink to="/sign-in" onClick={() => { setOpen(!open) }} className="positionLink"><img className="userIcon" src="/log-in.png" alt="login" />Sign In</NavLink>
                </ul>
            </div>}

            <NavLink to="/" onClick={() => { setActiveHome(!activeHome); setActive(false) }} className={(element) => element.isActive ? 'selectedHome' : 'home'}>

                {!activeHome ? < img src="./home2.png" className="homeIcon" alt="home" /> : <>
                    <NavLink to="/history">Search History</NavLink>
                </>}

            </NavLink>
            <NavLink to="/members" onClick={() => { setActiveHome(false) ; setActive(false)}} className={(element) => element.isActive ? 'selectedNetwork' : 'network'}>Network members</NavLink>
        </div>
    )
}


export default Navbar;