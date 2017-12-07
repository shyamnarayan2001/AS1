import React from "react";
import { Redirect } from "react-router-dom";
import { Container } from "../Container";
import { TextField } from "../../components/TextBox";
import { DropDown } from "../../components/DropDown";
import { ChooseModel}  from "../ChooseModel";
import { RadioGroup, Radio } from "../../components/Radio";
import { FileUpload } from "../FileUploadModal";
import { createModal } from "../../hoc/createModal";
import { fetchData } from "../../hoc/fetchData";
import { compose } from "../../utils";
import Separator from "../../components/Separator";
import Button from "../../components/Button";
import { StatusModal } from "../../sections/StatusModal";
import "./TestData.css";

export class TestDataState extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      file_type: "Choose file type",
      redirect: false,
      testHeaderData: [],
      file: "",
      path: "",
      testDataName: "",
      header: "n",
      fileType: "csv",
      chooseModel: "",
      //selectedAlgos: {},
      uploadFormData: {},
      identifier: "",
      feature: {},
      target: "",
      testType:"",
      showRunStatus: false
      //algorithmSettings: {}
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.submitTestForRun = this.submitTestForRun.bind(this);
    this.closeModalAndRedirect = this.closeModalAndRedirect.bind(this);
  }
  //controlling textbox and dropdown for file
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
  // handle file upload submit
  handleSubmit() {
    const formData = new FormData();
    formData.append("file", this.state.file);
    formData.append("testName", this.state.testDataName);
    formData.append("header", this.state.header);
    formData.append("modelName", this.state.chooseModel);
    formData.append("fileType", this.state.fileType.toLowerCase());
    this.props.fetchData("form", "/api/testHeader/", "testData", formData);
    this.props.handleClose("isOpen");
  }
  
  //handle run test
  submitTestForRun() {
    const payload={
      testName: this.state.testDataName,
      modelName: this.state.chooseModel,
      runType: this.state.testType
    }
    console.log(payload,"payload");
     this.props.fetchData(
      "post",
      "/api/runTest/",
      "runTestData",
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
          labelText="Name of the Test Data"
          name="testDataName"
          value={this.state.testDataName}
          handleChange={this.handleChange}
        />
        <ChooseModel
          groupName="Choose Model"
          style={{ padding: "10px", marginTop: "10px" }}
          align="horizontal"
          radioValue={this.state.chooseModel}
          handleChange = {this.handleChange}
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
          if (/testmodel/gi.test(child.type.displayName)) {
             const {
              status,
              responseData,
              errorMessage
            } = this.props.testData; 

            
           // console.log(this.props.testData.responseData);

            return React.cloneElement(child, {
              status: status,
              options: responseData,
              errorMessage: errorMessage,
            });
          } else {
            return child;
          }
        })}
        <section className="column-select">
          
          <Separator separatorText="OR" />
          <RadioGroup 
            name="testType"
            handleChange = {this.handleChange}
            radioValue = {this.state.testType}  
          >
            {[
              { labelText: "Type 1", name: "type1" },
              { labelText: "Type 2", name: "type2" }
            ].map((option, index) =>
              <Radio key={index} 
                {...option} 
                labelStyle={{ width: "45%" }}
                //handleChange={this.handleChange}
                value={option.name}  
              >
                <i className="info-icon" />
                <span className="moreinfo">Know More</span>
              </Radio>
            )}
          </RadioGroup>
        </section>
        <div className="run-section">
          <Button
            buttonText="RUN"
            style={{ width: "40%", margin: "0 auto", display: "block" }}
            handleClick={this.submitTestForRun}
          />
        </div>
         <StatusModal
          text={this.props.runTestData.errorMessage === "" ? "Test Data Is Successfully Submitted !!! Check Run Status..." : this.props.runTestData.errorMessage}
          isOpen={this.state.showRunStatus}
          closeModalRedirect={this.props.runTestData.errorMessage === "" ? this.closeModalAndRedirect : this.closeModal}
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

export default compose(
  fetchData(["modelData","testData","runTestData"]),
  createModal(["isOpen", "algoModal"])
)(TestDataState);
