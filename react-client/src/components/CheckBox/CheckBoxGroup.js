import React from "react";
import CheckBox from "./CheckBox";
import "./CheckBoxGroup.css";

class CheckBoxGroup extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.state = { [props.groupName]: {} };
  }
  handleChange(e) {
    const { name, checked } = e.target;
    const checkGroupData = this.state[this.props.groupName];
    this.setState({
      [this.props.groupName]: { ...checkGroupData, [name]: checked }
    });
  }
  render() {
    const { groupName, children, align } = this.props;
    //const checkGroupData = this.state[groupName];
    return (
      <div
        className={`checkbox-group checkbox-group-${align}`}
        style={this.props.style}
      >
        <h2>
          {groupName}
        </h2>
        <div className="checkbox-wrapper">
          {React.Children.map(children, child => {
            if (child.type === CheckBox) {
              return React.cloneElement(child, {
                handleChange: this.props.handleChange
                  ? this.props.handleChange
                  : this.handleChange
              });
            } else return child;
          })}
        </div>
      </div>
    );
  }
}

CheckBoxGroup.defaultProps = {
  align: "horizontal"
};

export default CheckBoxGroup;
