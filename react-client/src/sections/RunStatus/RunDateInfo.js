import React from "react";
import './RunDateInfo.css';

const RunDateInfo = props =>
  <div className="status-date-time">
    <div className="status-date">{props.date}</div>
    <div className="status-time">{props.time}</div>
  </div>;

export default RunDateInfo;
