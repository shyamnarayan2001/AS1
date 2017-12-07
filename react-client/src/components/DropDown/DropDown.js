import React from "react";
import "./DropDown.css";

const DropDown = props =>
  <div className="drop-down" style={props.style}>
    <label className="drop-down-label">
      {props.labelText}
    </label>
    <select
      name={props.name}
      className="drop-down-select"
      value={props.value}
      onChange={(event) => props.handleChange(event)}
      style={props.dropDownStyle}
    >
      <option key="default" value={props.defaultOption} disabled>{props.defaultOption}</option>
      {props.options.map((option, index) =>
        <option key={index} value={option}>
          {option}
        </option>
      )}
    </select>
  </div>;

export default DropDown;
