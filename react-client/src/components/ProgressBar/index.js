import React from "react";
import "./ProgressBar.css";

const ProgressBar = props =>
  <div className="progress-bar" style={props.style}>
    <div className="percentage">
      {props.percentage}%
    </div>
    <div className="status-bar">
      <div className="complete-bar" style={{width : `${props.percentage}%`}}/>
    </div>
  </div>;

export default ProgressBar;
