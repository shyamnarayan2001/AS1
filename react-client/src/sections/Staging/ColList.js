import React from 'react';
import './ColList.css';

const ColList = (props) => (
        <ul className="col-list">
          {props.children}
        </ul>
)

const ColItem = (props) => (
        <li className="col-item">
          {props.index+1}. {props.colName} <span className="col-link">Move to table</span>
        </li>
)

export { ColList , ColItem}
