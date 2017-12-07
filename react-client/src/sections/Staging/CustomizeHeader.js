import React from "react";
import { TextField } from "../../components/TextBox";
import Button from "../../components/Button";
import TextArea from "../../components/TextArea";
import "./CustomizeHeader.css";

const CustomizeHeader = props =>
  <div className="customize-header">
    <h2 className="font-bold customize-header-title">Customize a new header</h2>
    <TextField
      labelText="Name of variable/header"
      inputStyle={{ width: "60%" }}
    />
    <TextArea
      labelText="Features used in the Model"
      textAreaStyle={{ width: "85%" }}
    />
    <div>
      <Button buttonText="Add to new table" className="new-table-button"/>
    </div>
  </div>;

export default CustomizeHeader;
