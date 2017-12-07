import React from "react";
import Modal from "react-modal";
import { error, loader, noop } from "../../hoc/fetchData";
import { compose } from "../../utils";
import  Button from "../../components/Button";

export const StatusModal = props => {
  return (
    <Modal
      isOpen={props.isOpen}
      contentLabel="Select Algorithm"
      onRequestClose={props.closeModal}
      modalText={props.text}
      style={{
        content: {
          width: "45%",
          height: "35%",
          left: "50%",
          top: "50%",
          transform: "translate(-50%,-50%)"
        }
      }}
    >
      <EnhancedModalContent {...props} />
    </Modal>
  );
};

const ModalContent = props =>
<div style={{padding: "10%"}}>
    <div>
        <h5>{props.text}</h5>
    </div>
    
    <div style={{padding: "10px",width: "100%"}}>
      <Button
        buttonText="Ok"
        handleClick={props.closeModalRedirect}
        style={{margin: "0% 0% 0% 30%"}}   
    />
    </div>
</div>

const EnhancedModalContent = compose(
  noop("Please load ..."),
  loader("Submitting Model.."),
  error()
)(ModalContent);
