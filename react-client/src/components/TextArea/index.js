import React from "react";
import "./TextArea.css";

export default props =>
  <div className="textarea-container">
    <label className="text-area-label">
      {props.labelText}
    </label>
    <textarea style={props.textAreaStyle} className="custom-textarea"/>
  </div>;
