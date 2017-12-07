import React from "react";
import { NavLink } from "react-router-dom";
import "./HeaderItem.css";

const HeaderItem = props =>
  <NavLink className="header-item" to={props.linkPath} activeClassName="header-item header-active">
    <h2>{props.headerText}</h2>
    <p>{props.headerDescription}</p>
  </NavLink>;

HeaderItem.defaultProps = {
  linkPath: "/"
};

export default HeaderItem;
