import React from "react";
import "./Button.css";

const Button = props =>
  <button
    onClick={(event) => props.handleClick(event)}
    style={props.style}
    className={`button ${props.hover ? 'button-hover' : ''} ${props.className || ""}`}
  >
    {props.buttonText}
  </button>;

Button.defaultProps = {
        hover : true
}

export default Button;
