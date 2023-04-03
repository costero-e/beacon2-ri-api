import { NavLink } from 'react-router-dom';
import './Navbar.scss'
import React, { useState } from 'react';


function Navbar() {

    const [selected, setIsSelected ] = useState('')



     
    return (

        
    
            <nav id="nav">
                <div className="nav left">
                   
                    {!selected && 
                        <span className="gradient skew"><h1 className="logo un-skew"><a href="/">
                        < img src="./home2.png" className="homeIcon" alt="home" />
                    </a></h1></span>}

                    {selected && 
                        <span className="gradient2 skew"><h1 className="logo un-skew"><a href="/">
                        < img src="./home2.png" className="homeIcon" alt="home" />
                    </a></h1></span>}
                   
                </div>
                <div class="nav right">
                    <NavLink to= "/sign-up" className= {selected ? 'nav-link': 'nav-link'} onClick={() => { setIsSelected(true)}}><span className="nav-link-span"><span className="u-nav">Sign Up</span></span> </NavLink>
                    <NavLink to="/sign-in" className={selected ? 'nav-link': 'nav-link'} onClick={() => { setIsSelected(true)}}><span className="nav-link-span"><span className="u-nav">Sign In</span></span></NavLink>
                    <NavLink to="/members" className={selected ? 'nav-link': 'nav-link'} onClick={() => { setIsSelected(true)}}><span className="nav-link-span"><span className="u-nav">Network members</span></span></NavLink>
                </div>
            </nav>
        


    )
}


export default Navbar;