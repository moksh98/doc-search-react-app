import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
    return (
        <div className="footer">
            <div className="container">
                <br />
                <div className="row justify-content-center">
                    <div className="col-7 col-sm-5">
                        <h2 style={{color: 'white'}}><strong>NC STATE</strong></h2>
                        <h4 style={{color: 'white'}}>Humanities and Social Sciences</h4><br />
                        <h5 style={{color: 'white'}}>Khayrallah Center for Lebanese Diaspora Studies</h5><br />
                        <address style={{color: 'white'}}>
                        Campus Box 8013<br /><br />
                        North Carolina State University<br /><br />
                        Raleigh, NC 27695-8108<br /><br />
                        <i className="fa fa-phone fa-lg"></i>: 919-515-5058<br /><br />
                        <i className="fa fa-envelope fa-lg"></i>: <a href="mailto:lebanesestudies@ncsu.edu">
                        lebanesestudies@ncsu.edu</a>
                        </address>
                    </div>          
                    <div className="col-4 offset-1 col-sm-2">
                        <h5 style={{color: 'white'}}>Links</h5>
                        <ul className="list-unstyled">
                            <li><Link to="/home">Home</Link></li>
                            <li><Link to="aboutus">About</Link></li>
                            <li><Link to="/search">Search</Link></li>
                            <li><Link to="/browse">Browse</Link></li>
                            <li><Link to="/contactus">Contact</Link></li>
                        </ul>
                    </div>
                    <div className="col-12 col-sm-4 align-self-center">
                        <div className="text-center">
                            <a className="btn btn-social-icon btn-facebook" href="https://www.facebook.com/KhayrallahCenter"><i className="fa fa-facebook"></i></a> &ensp;
                            <a className="btn btn-social-icon btn-twitter" href="https://www.twitter.com/KhayrallahNCSU"><i className="fa fa-twitter"></i></a> &ensp;
                            <a className="btn btn-social-icon btn-instagram" href="https://instagram.com/khayrallahcenter"><i className="fa fa-instagram"></i></a> &ensp;
                            <a className="btn btn-social-icon btn-google" href="https://www.youtube.com/user/LebaneseNC"><i className="fa fa-youtube"></i></a> &ensp;
                            <a className="btn btn-social-icon btn-linkedin" href="https://www.linkedin.com/in/khayrallah-center-for-lebanese-diaspora-studies/"><i className="fa fa-linkedin"></i></a>
                        </div>
                    </div>
                </div>
                <br />
                <div className="row justify-content-center">             
                    <div className="col-auto">
                        <h5 style={{color: 'white'}}>© Copyright 2023 North Carolina State University</h5>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Footer;