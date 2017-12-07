import React from "react";
import { NavLink } from "react-router-dom";
import "./MenuItem.css";

const MenuItem = props => {
  return (
    <NavLink to={props.linkPath} className="menu-link" activeClassName="menu-active">
      <li className="menu-item">
        <i className={`icon ${props.menuIcon}`} />
        <span className="menu-text">
          {props.menuText}
        </span>
      </li>
    </NavLink>
  );
};

MenuItem.defaultProps = {
  menuText: "test"
};

export default MenuItem;
