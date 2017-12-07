import React from "react";
import MenuItem from "./MenuItem";
import "./Menu.css";

const Menu = props => {
  return (
    <ul className="menu">
      {props.menuItems.map((menuItem, index) =>
        <MenuItem key={index} {...menuItem} />
      )}
    </ul>
  );
};

export default Menu;
