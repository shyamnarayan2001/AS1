import React from "react";
import { Redirect } from "react-router-dom";
import { Container } from "../Container";
import { TextField } from "../../components/TextBox";
import { DropDown } from "../../components/DropDown";
import { FileUpload } from "../FileUploadModal";
import { createModal } from "../../hoc/createModal";
import { fetchData } from "../../hoc/fetchData";
import { StatusModal } from "../../sections/StatusModal";
import { compose } from "../../utils";
import R from "ramda";
// import CreateModel from "../CreateModel";
import Button from "../../components/Button";
import "./InputData.css";

const InputData = props =>
  <Container>
    <TextField labelText="Name of the model" name="model_name" />
    <DropDown
      labelText="File Type"
      value="Choose file type"
      name="file_type"
      options={["Excel/CSV", "PDF"]}
    />
    {props.children}
    {/* <div className="run-section">
      <Button
        buttonText="RUN"
        style={{ width: "40%", margin: "0 auto", display: "block" }}
      />
    </div> */}
  </Container>;

export class InputDataState extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      file_type: "Choose file type",
      redirect : false,
      headerData: [],
      file: "",
      path: "",
      modelName: "",
      header: "n",
      fileType: "csv",
      selectedAlgos: {},
      uploadFormData: {},
      identifier: "",
      feature: {},
      target: "",
      algorithmSettings: {}
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleCheckBox = this.handleCheckBox.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.submitModelForRun = this.submitModelForRun.bind(this);
    this.closeModalAndRedirect = this.closeModalAndRedirect.bind(this);
    this.closeModal = this.closeModal.bind(this);
  }

  componentDidMount() {
    if (sessionStorage.getItem("headerFormData")) {
      const headerFormData = JSON.parse(
        sessionStorage.getItem("headerFormData")
      );
      this.setState(headerFormData);
    }
    if (sessionStorage.getItem("headerData")) {
      const headerData = JSON.parse(sessionStorage.getItem("headerData"));
      this.props.setStateData("headerData", headerData);
    }
  }

  componentWillUnmount() {
    sessionStorage.setItem(
      "headerFormData",
      JSON.stringify({
        file: this.state.file,
        path: this.state.path,
        header: this.state.header,
        fileType: this.state.fileType,
        file_type: this.state.file_type,
        selectedAlgos: {},
        identifier: {},
        feature: {},
        target: {},
        modelName: this.state.modelName,
        showRunStatus: false
      })
    );

    sessionStorage.setItem("headerData", JSON.stringify(this.props.headerData));
  }

  handleSubmit() {
    const formData = new FormData();
    formData.append("file", this.state.file);
    formData.append("modelName", this.state.modelName);
    formData.append("header", this.state.header);
    formData.append("fileType", this.state.fileType.toLowerCase());
    this.props.fetchData("form", "/api/header/", "headerData", formData);
    this.props.handleClose("isOpen");
  }

  handleCheckBox(groupName, event) {
    const { name, checked } = event.target;
    this.setState(
      { [groupName]: { ...this.state[groupName], [name]: checked } },
      () => {
        if (name === "algorithm_settings" && checked) {
          // const algoFormData = new FormData();
          // algoFormData.append("modelName", this.state.modelName);
          var identifier = "";
          if (Object.keys(this.state.identifier).length === 0) {
            identifier = "n";
          } else {
            identifier = Object.keys(this.state.identifier)[0];
          }
          const algoFormData = {
            modelName: this.state.modelName,
            identifier: identifier,
            features: Object.keys(this.state.feature).filter(R.identity),
            target: Object.keys(this.state.target)[0]
          };
          console.log("settings", algoFormData);
          this.props.fetchData(
            "post",
            "/api/algorithmSettings/",
            "algorithmData",
            algoFormData
          );
          this.props.handleOpen("algoModal");
        }
        // if(groupName === "Algorithms"){
        //   selectedAlgos :
        // }
      }
    );
  }

  handleChange(event) {
    const { name, value, type } = event.target;

    if (type === "file") {
      const { files: [file], value } = event.target;
      this.setState({
        file: file,
        path: value
      });
    } else {
      this.setState({ [name]: value }, () => {
        if (
          this.state.file_type.toLowerCase() === "excel/csv" &&
          type === "select-one"
        )
          this.props.handleOpen("isOpen");
      });
    }
  }
  //creating payload for submission
  submitModelForRun() {
    var algo_names = [];
    var identifier = "";
    if (Object.keys(this.state.identifier).length === 0) {
      identifier = "n";
    } else {
      identifier = Object.keys(this.state.identifier)[0];
    }
    if (
      Object.keys(this.state.selectedAlgos)
        .filter(R.identity)
        .indexOf("algorithm_settings") === -1
    ) {
      algo_names="Not Selected";
    } else {
      algo_names = Object.keys(this.state.algorithmSettings).filter(R.identity);
    }
    const payload = {
      modelName: this.state.modelName,
      identifier: identifier,
      features: Object.keys(this.state.feature).filter(R.identity),
      target: Object.keys(this.state.target)[0],
      algorithm_names: algo_names
    };
    console.log(payload, "Payload");
    this.props.fetchData(
      "post",
      "/api/runTraining/",
      "runTrainingData",
      payload
    );
    this.setState({ showRunStatus: true });
  }
  //method for closing modal and to redirect
  closeModalAndRedirect() {
    this.setState({
      showRunStatus: false,redirect:true
    });
  }
  closeModal() {
    this.setState({
      showRunStatus: false,redirect:false
    });
  }

  render() {
    if (this.state.redirect)
      return (
        <Redirect
          to={{
            pathname: "/runstatus"
          }}
        />
      );
    return (
      <Container>
        <TextField
          labelText="Name of the model"
          name="modelName"
          value={this.state.modelName}
          handleChange={this.handleChange}
        />
        <DropDown
          labelText="File Type"
          value={this.state.file_type}
          defaultOption="Choose file type"
          handleChange={this.handleChange}
          name="file_type"
          options={["Excel/CSV", "PDF"]}
        />
        {React.Children.map(this.props.children, child => {
          if (/createmodel/gi.test(child.type.displayName)) {
            const {
              status,
              responseData,
              errorMessage
            } = this.props.headerData;

            return React.cloneElement(child, {
              status: status,
              options: responseData,
              algoModal: this.props.algoModal,
              algorithmData: this.props.algorithmData,
              errorMessage: errorMessage,
              openAlgoModal: () => this.props.handleOpen("algoModal"),
              closeAlgoModal: () => this.props.handleClose("algoModal"),
              handleCheckBox: R.curry(this.handleCheckBox),
              selectedAlgos: this.state.selectedAlgos,
              identifier: this.state.identifier,
              feature: this.state.feature,
              target: this.state.target
            });
          } else {
            return child;
          }
        })}
        <div className="run-section">
          <Button
            buttonText="RUN"
            style={{ width: "40%", margin: "0 auto", display: "block" }}
            handleClick={this.submitModelForRun}
          />
        </div>
        <StatusModal
          text={this.props.runTrainingData.errorMessage === "" ? "Model Is Successfully Submitted !!! Check Run Status..." : this.props.runTrainingData.errorMessage}
          isOpen={this.state.showRunStatus}
          closeModalRedirect={this.props.runTrainingData.errorMessage === "" ? this.closeModalAndRedirect : this.closeModal}
        />
        <FileUpload
          {...this.state}
          isOpen={this.props.isOpen}
          handleChange={this.handleChange}
          handleSubmit={this.handleSubmit}
          closeModal={this.props.handleClose.bind(this, "isOpen")}
        />
      </Container>
    );
  }
}

export const InputDataContainer = compose(
  fetchData(["headerData", "algorithmData", "runTrainingData"]),
  createModal(["isOpen", "algoModal"])
)(InputDataState);

export default InputData;
