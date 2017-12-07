import "./SearchBox.css";
import React from "react";

const SearchBox = props =>
  <div className="search-box-container" style={props.style}>
    <input
      type="text"
      name={props.name}
      className="search-box"
      style={props.inputStyles}
      placeholder={props.labelText}
    />
  </div>;

export default SearchBox;
