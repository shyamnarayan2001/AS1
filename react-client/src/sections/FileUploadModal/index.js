import Modal from "react-modal";
import React from "react";
import { RadioGroup, Radio } from "../../components/Radio";
import { FileInput } from "../../components/FileInput";
import { TextField } from "../../components/TextBox";
import Button from "../../components/Button";
import "./FileUploadModal.css";
// import { compose }  from "../../utils";
// import { createModal } from "../../hoc/createModal";

export class FileUpload extends React.Component {
  constructor(props) {
    super(props);
    this.state = { file: "", path: "" };
    // this.handleFormChange = this.handleFormChange.bind(this);
    // this.handleSubmit = this.handleSubmit.bind(this);
    // this.handleFilePath = this.handleFilePath.bind(this);
  }

  render() {
    return (
      <Modal
        isOpen={this.props.isOpen}
        onRequestClose={this.props.closeModal}
        contentLabel="file upload modal"
        style={{
          content: {
            width: "40%",
            left: "40%",
            top: "30%",
            height: "50%"
          }
        }}
      >
        <div className="file-upload">
          <h3 className="description">
            Choose your option and include the respective file for further
            anaylsis
          </h3>
          <RadioGroup
            name="fileType"
            className="file-upload-radio"
            radioValue={this.props.fileType}
            style={{ padding: "20px" }}
            labelText="File Type"
            handleChange={event => this.props.handleChange(event)}
          >
            <Radio
              labelText="Excel"
              value="Excel"
              style={{ width: "25%" }}
              labelStyle={{ width: "100%" }}
            />
            <Radio
              labelText="CSV"
              value="CSV"
              style={{ width: "25%" }}
              labelStyle={{ width: "100%" }}
            />
          </RadioGroup>
          <div className="group file-input-form">
            <h2
              className="font-bold"
              style={{
                verticalAlign: "middle",
                display: "inline-block",
                marginRight: "10px"
              }}
            >
              Browse File
            </h2>
            <TextField
              style={{
                display: "inline-block",
                width: "40%",
                verticalAlign: "middle",
                padding: "0px"
              }}
              readOnly={true}
              value={this.props.path}
              inputStyle={{
                width: "100%",
                height: "36px",
                borderRadius: "0px",
                marginTop: "0px"
              }}
            />
            <FileInput labelText="Browse" handleChange={(event) =>  this.props.handleChange(event)} />
          </div>
          <RadioGroup
            name="header"
            radioValue={this.props.header}
            className="file-upload-radio"
            handleChange={event => this.props.handleChange(event)}
            style={{ padding: "20px" }}
            labelText="Header"
          >
            <Radio
              labelText="Yes"
              value="y"
              style={{ width: "25%" }}
              labelStyle={{ width: "100%" }}
            />
            <Radio
              labelText="No"
              value="n"
              style={{ width: "25%" }}
              labelStyle={{ width: "100%" }}
            />
          </RadioGroup>
          <div className="button-group">
            <Button
              buttonText="Submit"
              className="submit-button"
              handleClick={() => this.props.handleSubmit()}
            />
            <Button
              buttonText="Cancel"
              className="cancel-button"
              hover={false}
              handleClick={() => this.props.closeModal()}
            />
          </div>
        </div>
      </Modal>
    );
  }
}
