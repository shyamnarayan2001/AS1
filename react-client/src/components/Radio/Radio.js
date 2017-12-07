import React from "react";
import PropTypes from "prop-types";
import "./Radio.css";

class RadioGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = { [props.name]: "" };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    const { name } = this.props;
    const { value } = e.target;
    if (this.props.handleChange) this.props.handleChange(e);
    else this.setState({ [name]: value });
  }
  render() {
    const { name, children, labelText, autoWidth } = this.props;

    const currentSelection = this.props.handleChange
      ? this.props.radioValue
      : this.state[name];
    const dynamicWidth = 1 / React.Children.count(children) * 100;
    return (
      <div
        className={`radio-group ${this.props.className || ""}`}
        style={this.props.style}
      >
        <h2 className="radio-group-label">
          {labelText}
        </h2>
        <div className="radio-group-button">
          {React.Children.map(children, radioComp => {
            if (radioComp.type === Radio) {
              const isChecked = radioComp.props.value === currentSelection;
              return React.cloneElement(radioComp, {
                handleChange: this.handleChange,
                name: name,
                style: !autoWidth
                  ? radioComp.props.style
                  : Object.assign({}, radioComp.props.style, {
                      width: `${dynamicWidth}%`
                    }),
                isChecked
              });
            } else {
              return radioComp;
            }
          })}
        </div>
      </div>
    );
  }
}

RadioGroup.defaultProps = {
  autoWidth: true
};

export const Radio = props =>
  <div className="radio-custom" style={props.style}>
    <input
      type="radio"
      name={props.name}
      className="radio-custom-button"
      id={props.labelText}
      checked={props.isChecked}
      value={props.value ? props.value : props.labelText}
      style={props.inputStyle}
      onChange={props.handleChange}
    />
    <label
      className="radio-custom-label"
      htmlFor={props.labelText}
      style={props.labelStyle}
    >
      {props.labelText}
      {props.children}
    </label>
  </div>;

Radio.propTypes = {
  value: PropTypes.string.isRequired,
  labelText: PropTypes.string.isRequired,
  style: PropTypes.object,
  handleChange: PropTypes.func
};

export default RadioGroup;
