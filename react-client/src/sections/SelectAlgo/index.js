import React from "react";
import Modal from "react-modal";
import { CheckBoxGroup, CheckBox } from "../../components/CheckBox";
import { error, loader, noop } from "../../hoc/fetchData";
import { compose } from "../../utils";
import  Button from "../../components/Button";

const SelectAlgo = props => {
  return (
    <Modal
      isOpen={props.isOpen}
      contentLabel="Select Algorithm"
      onRequestClose={props.closeModal}
      style={{
        content: {
          width: "45%",
          height: "60%",
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
  <div>
    <h2 style={{ paddingBottom: "20px" }}>
      Choose the Algorithm which need to run for this Test.
    </h2>
    <CheckBoxGroup
      groupName="Algorithms"
      handleChange={props.handleCheckBox}
      style={{ padding: "20px", background: "#f1f1f1" }}
    >
      {props.responseData.map((item, index) =>
        <CheckBox
          
          key={index}
          labelText={item}
          htmlId={item}
          name={item}
          value={props.value}
          
          style={{ display: "inline-block", width: "50%", padding: "10px" }}
        />
      )}
    </CheckBoxGroup>
    <div style={{padding: "10px",width: "100%"}}>
      <Button
        buttonText="Ok"
        handleClick={props.closeModal}
        style={{margin: "0% 0% 0% 30%"}}   
    />
    </div>
    
  </div>;

const EnhancedModalContent = compose(
  noop("Please load ..."),
  loader("Fetching Algorithms.."),
  error()
)(ModalContent);

SelectAlgo.defaultProps = {
  responseData: [
      "Linear Regression",
      "Ridge Regression",
      "Support Vector Machine",
      "Neural Network",
      "Gradient Boosting",
      "Ada Boosting"
  ]
  
};

export default SelectAlgo;
