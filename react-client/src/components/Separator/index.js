import React from 'react';
import './Separator.css';

const Separator = (props) => (
      <h2 className="outer-text">
        <span className="inner-text">{props.separatorText}</span>
      </h2>
)

export default Separator;
