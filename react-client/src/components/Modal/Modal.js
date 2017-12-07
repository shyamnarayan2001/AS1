import React from "react";
import "./Modal.css";

const Modal = props =>
  <div
    className="modal"
    style={props.isOpen ? { display: "block" } : { display: "none" }}
  >
    <div className="modal-content">
      {props.children}
    </div>
  </div>;

export default Modal;
