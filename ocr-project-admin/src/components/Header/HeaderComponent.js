import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faArrowRight,
} from "@fortawesome/free-solid-svg-icons";
import logo from "../../assets/images/logo.svg";

export default function Header() {
  return (
    <div style={{ backgroundColor: "#E5E5E5", paddingBottom: '40px' }}>
      <div className="row">
        <div
          className="col-2"
          style={{
            display: "flex",
            justifyContent: "center",
            padding: "6px 16px",
            marginTop: "40px",
            marginLeft: "40px",
          }}
        >
          <button className="btn btn-danger" style={{ color: "#CC0000" }}>
            <span style={{ color: "#FFFFFF" }}>Give Now</span>&nbsp;&nbsp;
            <FontAwesomeIcon style={{ color: "#FFFFFF" }} icon={faArrowRight} />
          </button>
        </div>
        <div
          className="col-7"
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "32px",
          }}
        >
          <img src={logo} alt="logo" />
        </div>
        <div
          className="col-2"
          style={{
            display: "flex",
            justifyContent: "center",
            padding: "2px 16px 10px",
            marginTop: "40px",
            marginRight: "40px",
          }}
        >
          <button className="btn btn btn-outline-dark">عربى</button>
        </div>
      </div>
    </div>
  );
}
