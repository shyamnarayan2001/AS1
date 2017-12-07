import React from "react";
import "./TextBox.css";

const TextField = props =>
  <div className={`text-box ${props.className || ""}`} style={props.style}>
    <label htmlFor={props.name}>
      {props.labelText}
    </label>
    <input
      type="text"
      name={props.name}
      value={props.value}
      readOnly={props.readOnly}
      onChange={event => props.handleChange(event)}
      id={props.name}
      className="text-field"
      style={props.inputStyle}
    />
    {props.children}
  </div>;

export default TextField;
