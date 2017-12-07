import React from 'react';
import './Column.css';

const Col = (props) => (
  <div className={`col-1-${props.count}`} style={props.style}>
      {props.children}
  </div>
)

export default Col;
