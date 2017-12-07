import React from "react";
import TestDataContainer from "../TestData";
import { loader, error, noop } from "../../hoc/fetchData";
import { compose } from "../../utils";
import { CheckBoxGroup, CheckBox } from "../../components/CheckBox";

const listToObj = inputList => {
  return inputList.reduce((acc, curr) => {
    return { ...acc, [curr]: true };
  }, {});
};
const TestModelContent = props => {
  const { options: { features, identifier, target } } = props;
  console.log(features, identifier, target);  
  const featureObj = listToObj(features);
  const identifierObj = listToObj(Array.isArray(identifier) ? identifier : []);
  const targetObj = listToObj([target]);
  return (
    <div>
      {[
        { groupName: "Identifier", name: "identifier" },
        { groupName: "Feature Selection", name: "feature" },
        { groupName: "Target", name: "target" }
      ].map(({ groupName, name }, index) =>
        <CheckBoxGroup
          align="vertical"
          key={index}
          groupName={groupName}
          style={{ maxHeight: "300px", overflow: "auto", paddingRight: "20px" }}
        >
          {props.options.header.map((headerItem, index) => {
            
            let isDisabled = false;
            if (name === "feature") {
              isDisabled = featureObj.hasOwnProperty(headerItem);
            } else if (name === "identifier") {
              isDisabled = identifierObj.hasOwnProperty(headerItem);
            } else {
              isDisabled = targetObj.hasOwnProperty(headerItem);
            }
            return (
              <CheckBox
                style={{ display: "block", textAlign: "left" }}
                labelText={headerItem}
                key={`${groupName} ${index}`}
                value={isDisabled} // need to apply logic
                name={headerItem}
                disabled={true}
                htmlId={`${groupName} ${index}`}
              />
            );
          })}
        </CheckBoxGroup>
      )}
    </div>
  );
};

TestModelContent.defaultProps = {
  options: []
};

const EnhancedTestModel = compose(
  noop("Please upload file"),
  loader("Getting Headers.."),
  error()
)(TestModelContent);

const CreateModel = props =>
  <TestDataContainer>
    <EnhancedTestModel />
  </TestDataContainer>;

export default CreateModel;
