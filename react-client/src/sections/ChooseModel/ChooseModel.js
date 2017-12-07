import React from "react";
import { SearchBox } from "../../components/TextBox";
import { Radio, RadioGroup } from "../../components/Radio";
import { compose } from "../../utils";
import { fetchData } from "../../hoc/fetchData";
import "./ChooseModel.css";

export class ChooseModel extends React.Component {
  
  //loading modelData at starting
  componentDidMount() {
    this.props.fetchData("get", "/api/getAllModels/", "modelData", "get");
  }

  render() {
    return (
      <div className="choose-model-group" style={this.props.style}>
        <SearchBox
          style={{
            position: "absolute",
            top: "5px",
            right: "5px"
          }}
          inputStyles={{ backgroundColor: "#ebf0f5", width: "100%" }}
        />
        <div style={{ marginTop: "5%", marginLeft: "0%" }}>
          <RadioGroup
            name="chooseModel"
            radioValue={this.props.radioValue}
            labelText="Choose Model"
            autoWidth={false}
            handleChange={event => this.props.handleChange(event)}
          >
            {this.props.modelData.responseData.map((option, index) =>
              <Radio
                key={index}
                labelStyle={{ width: "100%" }}
                style={{ width: "25%" }}
                labelText={option.modelName}
                value={option.modelName}
              />
            )}
          </RadioGroup>
        </div>
      </div>
    );
  }
}
export default compose(fetchData(["modelData"]))(ChooseModel);
