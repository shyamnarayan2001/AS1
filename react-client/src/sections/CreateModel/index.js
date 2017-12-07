import React from "react";
import { InputDataContainer } from "../InputData";
import { loader, error, noop } from "../../hoc/fetchData";
import { compose } from "../../utils";
import { CheckBoxGroup, CheckBox } from "../../components/CheckBox";
import SelectAlgo from "../SelectAlgo";
import R from "ramda";

const algoOptions = [
  {
    labelText: "Feature Elimination",
    name: "feature_elimination",
    id: "feature_elimination"
  },
  {
    labelText: "Feature Importance",
    name: "feature_importance",
    id: "feature_importance"
  },
  {
    labelText: "Algorithm Settings",
    name: "algorithm_settings",
    id: "algorithm_settings"
  },
  { labelText: "Accuracy", name: "accuracy", id: "accuracy" },
  { labelText: "Save Model", name: "save_model", id: "save_model" }
];

const checkDisability = (name, keyName, props) => {
  if (name === "target") return R.propOr(false, keyName, props.feature);
  else return false;
};
const CreateModelContent = props =>
  <div>
    {[
      { groupName: "Identifier", name: "identifier" },
      { groupName: "Feature Selection", name: "feature" },
      { groupName: "Target", name: "target" }
    ].map(({ groupName, name }, index) =>
      <CheckBoxGroup
        align="vertical"
        key={index}
        handleChange={props.handleCheckBox(name)}
        groupName={groupName}
        style={{ maxHeight: "300px", overflow: "auto", paddingRight: "20px" }}
      >
        {props.options.map((headerItem, index) => {
          return (
            <CheckBox
              style={{ display: "block", textAlign: "left" }}
              labelText={headerItem}
              key={`${groupName} ${index}`}
              value={props[name][headerItem] || false}
              name={headerItem}
              disabled={checkDisability(name, headerItem, props)}
              htmlId={`${groupName} ${index}`}
            />
          );
        })}
      </CheckBoxGroup>
    )}
    <CheckBoxGroup
      align="horizontal"
      groupName="Choose Model"
      style={{ paddingTop: "30px" }}
      handleChange={props.handleCheckBox("selectedAlgos")}
    >
      {algoOptions.map((algoItem, index) =>
        <CheckBox
          {...algoItem}
          key={index}
          value={props.selectedAlgos[algoItem.name] || false}
          htmlId={algoItem.id}
          style={{ display: "inline-block", width: "20%" }}
        />
      )}
    </CheckBoxGroup>
    <SelectAlgo
      isOpen={props.algoModal}
      handleCheckBox={props.handleCheckBox('algorithmSettings')}
      closeModal={props.closeAlgoModal}
      {...props.algorithmData}
    />
  </div>;

CreateModelContent.defaultProps = {
  options: []
  
};

const EnhancedCreateModel = compose(
  noop("Please upload file"),
  loader("Getting Headers.."),
  error()
)(CreateModelContent);

const CreateModel = props =>
  <InputDataContainer>
    <EnhancedCreateModel />
  </InputDataContainer>;

export default CreateModel;
