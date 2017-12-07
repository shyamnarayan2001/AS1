import React from "react";
import { wrapDisplayName } from "../utils";

export const createModal = (stateNames = []) => BaseComponent => {
  class CreateModal extends React.Component {
    constructor(props) {
      super(props);
      const initialState = stateNames.reduce(
        (acc, curr) => ({ ...acc, [curr]: false }),
        {}
      );
      this.state = initialState;
      this.handleClose = this.handleClose.bind(this);
      this.handleOpen = this.handleOpen.bind(this);
    }
    handleClose(stateName) {
      return this.setState({ [stateName]: false });
    }
    handleOpen(stateName) {
      return this.setState({ [stateName]: true });
    }
    render() {
      return (
        <BaseComponent
          {...this.state}
          {...this.props}
          handleOpen={this.handleOpen}
          handleClose={this.handleClose}
        />
      );
    }
  }
  CreateModal.displayName = wrapDisplayName(BaseComponent, "CreateModal");
  return CreateModal;
};
