import React from "react";
import { Container } from "../Container";
import { TextField } from "../../components/TextBox";
import TextArea from "../../components/TextArea";
import Col from "../../components/Col";
import Button from "../../components/Button";
import "./Models.css";

export default props =>
  <Container>
    <div className="form-1">
      <Col count={2}>
        <TextField
          labelText="Name of the model/Test/Predict"
          className={"model-test-name"}
          inputStyle={{ width: "100%" }}
        />
      </Col>
      <Col count={3}>
        <Button buttonText="VIEW MODEL" className="view-model" />
      </Col>
    </div>
    <div>
        <TextArea labelText="Features used in model" />
    </div>
    <div>
        <TextField labelText="Algorithm" />
    </div>
    <div>
        <TextField labelText="Other Settings" />
    </div>
    <div>
      <Button buttonText="VIEW RESULTS" className="view-results"/>
    </div>
  </Container>;
