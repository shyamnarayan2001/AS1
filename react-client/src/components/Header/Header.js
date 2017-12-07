import React from "react";
import HeaderItem from "./HeaderItem";
import "./Header.css";

const Header = props => {
  return (
    <div className="header">
      {props.headerItems.map((item, index) =>
        <HeaderItem {...item} key={index} />
      )}
    </div>
  );
};

export default Header;
