import React from "react";
import PredictDataContainer from "../PredictData";
import { loader, error, noop } from "../../hoc/fetchData";
import { compose } from "../../utils";
import { CheckBoxGroup, CheckBox } from "../../components/CheckBox";


const listToObj = inputList => {
  return inputList.reduce((acc, curr) => {
    return { ...acc, [curr]: true };
  }, {});
};
const PredictModelContent = props => {
  const { options: { features, identifier } } = props;
  console.log(features, identifier);  
  const featureObj = listToObj(features);
  const identifierObj = listToObj(Array.isArray(identifier) ? identifier : []);
  return (
    <div>
      {[
        { groupName: "Identifier", name: "identifier" },
        { groupName: "Feature Selection", name: "feature" }
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
            } else {
              isDisabled = identifierObj.hasOwnProperty(headerItem);
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

PredictModelContent.defaultProps = {
  options: []
};

const EnhancedPredictModel = compose(
  noop("Please upload file"),
  loader("Getting Headers.."),
  error()
)(PredictModelContent);

const PredictModel = props =>
  <PredictDataContainer>
    <EnhancedPredictModel />
  </PredictDataContainer>;

export default PredictModel;
