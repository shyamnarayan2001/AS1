import React from "react";
import "./CheckBox.css";

const CheckBox = props =>
  <div style={props.style}>
    <input
      type="checkbox"
      className="checkbox-custom"
      id={props.htmlId}
      name={props.name}
      checked={props.value}
      disabled={props.disabled}
      onChange={e => {
        // console.log(e.target);
        props.handleChange(e);
      }}
    />
    <label
      htmlFor={props.htmlId}
      className={`checkbox-custom-label ${props.disabled
        ? "checkbox-disabled"
        : ""}`}
    >
      {props.labelText}
    </label>
    {props.children}
  </div>;

CheckBox.defaultProps = {
  disabled: false
};

export default CheckBox;
