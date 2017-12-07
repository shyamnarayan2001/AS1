import React from "react";
import { wrapDisplayName } from "../utils";

export const handleForm = formEleType => BaseComponent => {
  class HandleForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = { [props.name]: "" };
      this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
      const { name, value } = event.target;
      this.setState({ [name]: value });
    }
    render() {
      return <BaseComponent handleChange={this.handleChange} />;
    }
  }

  HandleForm.displayName = wrapDisplayName(BaseComponent, "HandleForm");
  return HandleForm;
};
