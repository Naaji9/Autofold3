import React from 'react';
import './Footer.css';
import smallLogo1 from '../assets/smallLogo1.png';  // Replace with your actual logo paths


function Footer() {
    return (
        <footer className="App-footer">
            <div className="footer-content">
            <img src={smallLogo1} alt="Small Logo 1" className="footer-logo" />
                <p>&copy; {new Date().getFullYear()} Combi-l Lab. All rights reserved.</p>

            </div>
        </footer>
    );
}

export default Footer;
