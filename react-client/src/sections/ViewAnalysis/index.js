import React from "react";
import Modal from "react-modal";
import { error, loader, noop } from "../../hoc/fetchData";
import { compose } from "../../utils";
import { MediaBox, Row, Col } from "react-materialize";
import "./style.css";

export const ViewAnalysis = props => {
  return (
    <Modal
      isOpen={props.isOpen}
      contentLabel="Select Algorithm"
      onRequestClose={props.closeModal}
      modalText={props.text}
      style={{
        content: {
          width: "90%",
          height: "90%",
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

const GraphContent = props =>
  <div style={{ padding: "10px" }}>
    <div style={{ marginLeft: "99%" }}>
      <span style={{ cursor: "pointer" }} onClick={props.closeViewAnalysis}>
        X
      </span>
    </div>
    {console.log(props.graphData)}
    <Row>
      <Col m={12}>
        {props.graphData.map((data, index) =>
          <div className="inline">
            <MediaBox
              key={index}
              src={"http://localhost:8000" + data[1]}
              caption={data[0]}
              width="250"
            />
            <p>{data[0]}</p>
          </div>
        )}
        <div className="clearBoth"></div>
      </Col>
    </Row>
    {/* <div>
        <h5>{props.text}</h5>
    </div>
    
    <div style={{padding: "10px",width: "100%"}}>
      <Button
        buttonText="Ok"
        handleClick={props.closeModalRedirect}
        style={{margin: "0% 0% 0% 30%"}}   
    />
    </div> */}
  </div>;

const EnhancedModalContent = compose(
  noop("Please load ..."),
  loader("Submitting Model.."),
  error()
)(GraphContent);
