import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import '../Footer.css'
import {
  faFacebookSquare,
  faTwitterSquare,
  faInstagramSquare,
  faLinkedin,
  faYoutubeSquare,
} from "@fortawesome/free-brands-svg-icons";
function Footer() {
  return (
    <div className="footer" style={{ backgroundColor: "#fff", marginTop: 'auto', paddingBottom: '40px' }}>
      <div className="row">
        <div
          className="col"
          style={{
            marginTop: "2%",
            marginLeft: "8%",
            textAlign: "left",
            fontFamily: "Roboto",
            fontStyle: "normal",
            fontWeight: "700",
            fontSize: "18px",
            lineHeight: "160%",
            color: "#12394D",
          }}
        >
          <p>Khayrallah Center for Lebanese and Diaspora Studies</p>
        </div>
        <div
            className="col social-media-icons"
            style={{
              marginTop: "2%",
              marginRight: '8%',
              textAlign: 'right'

            }}
          >
            <a
              href="https://www.facebook.com/KhayrallahCenter"
              data-ua-label="Facebook"
            >
              <FontAwesomeIcon icon={faFacebookSquare} alt="Facebook" style={{ marginRight: "25px", color: "#CC0000",
              fontSize: "2rem"}}/>
            </a>

            <a
              href="https://www.twitter.com/KhayrallahNCSU"
              data-ua-label="Twitter"
            >
              <FontAwesomeIcon icon={faTwitterSquare} alt="Twitter" style={{ marginRight: "25px", color: "#CC0000",
              fontSize: "2rem"}}/>
            </a>

            <a
              href="https://www.instagram.com/khayrallahcenter/"
              data-ua-label="Instagram"
            >
              <FontAwesomeIcon icon={faInstagramSquare} alt="Instagram" style={{ marginRight: "25px", color: "#CC0000",
              fontSize: "2rem"}}/>
            </a>

            <a
              href="https://www.linkedin.com/company/moise-a-khayrallah-center-for-lebanese-diaspora-studies/"
              data-ua-label="LinkedIN"
            >
              <FontAwesomeIcon icon={faLinkedin} alt="LinkedIN" style={{ marginRight: "25px", color: "#CC0000",
              fontSize: "2rem"}}/>
            </a>

            <a
              href="https://www.youtube.com/@LebaneseNC"
              data-ua-label="Youtube"
            >
              <FontAwesomeIcon icon={faYoutubeSquare} alt="Youtube" style={{ marginRight: "0px", color: "#CC0000",
              fontSize: "2rem"}}/>
            </a>
          </div>
      </div>
      <div className="row">
        <div
          className="col"
          style={{
            textAlign: "left",
            marginLeft: "8%",
            fontFamily: "Roboto",
            fontStyle: "normal",
            fontWeight: "400",
            fontSize: "15px",
            lineHeight: "150%",
            color: "#666666",
          }}
        >
          Campus Box 8013 <br /> 
          North Carolina State University <br /> 
          Raleigh, NC 27695-8108 <br />
          919.515.5058 <br />{" "}
          <a
            href="mailto:lebanesestudies@ncsu.edu"
            style={{
              color: "#CC0000",
              fontWeight: "700",
              textDecoration: "none",
            }}
          >
            lebanesestudies@ncsu.edu
          </a>
        </div>
        <div
          className="col"
          style={{
            textAlign: "right",
            marginTop: '85px',
            marginRight: '8%',
            fontFamily: "Roboto",
            fontStyle: "normal",
            fontWeight: "400",
            fontSize: "16px",
            lineHeight: "150%",
            color: "#666666",
          }}
        >
          Copyright © 2023 NC State University. All rights reserved.{" "}
          {/* eslint-disable-next-line */}
          <a
            href="#"
            style={{
              color: "#CC0000",
              fontWeight: "700",
              textDecoration: "none",
            }}
          >
            Privacy Policy
          </a>
        </div>
      </div>
    </div>
  );
}

export default Footer;
