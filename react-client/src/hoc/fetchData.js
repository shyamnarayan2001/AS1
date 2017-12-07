import React, { Component } from "react";
import {
  postData,
  postFormData,
  getData,
  makeCancelable,
  wrapDisplayName
} from "../utils";
import { fetchEnum } from "./constants";
import eclipse from "../static/img/eclipse.svg";
import "./status.css";
import R from "ramda";

export const fetchData = (fetchFor = []) => BaseComponent => {
  class FetchData extends Component {
    constructor(props) {
      super(props);
      const initialState = fetchFor.reduce(
        (acc, curr) => ({
          ...acc,
          [curr]: { status: fetchEnum.noop, errorMessage: "", responseData: [] }
        }),
        {}
      );
      this.state = initialState;
      this.fetchData = this.fetchData.bind(this);
      this.fetchHelper = this.fetchHelper.bind(this);
      this.setStateData = this.setStateData.bind(this);
      this._isMounted = null;
      this._fetchPromise = null;
    }
    setStateData(keyName, data) {
      this.setState({ [keyName]: { ...this.state[keyName], ...data } });
    }
    fetchHelper(url, payload, keyName, applicativeFunction) {
      this.setState({
        [keyName]: { ...this.state[keyName], status: fetchEnum.initiate }
      });
      if(this.payload === 'get'){
        this._fetchPromise = makeCancelable(applicativeFunction(url));
      }
      else{
        this._fetchPromise = makeCancelable(applicativeFunction(url, payload));
      }
      
      this._fetchPromise.promise
        .then(data => {
          if (data.error) {
            this.setState({
              [keyName]: {
                ...this.state[keyName],
                status: fetchEnum.error,
                errorMessage: data.error
              }
            });
            return;
          }
          this.setState({
            [keyName]: {
              ...this.state[keyName],
              status: fetchEnum.completed,
              responseData: data
            }
          });
        })
        .catch(error => {
          if (error.isCanceled || !this._isMounted) return;
          console.error(error.message, error.stack);
          this.setState({
            [keyName]: {
              ...this.state[keyName],
              status: fetchEnum.error,
              errorMessage: error.message
            }
          });
        });
    }

    fetchData(method, url, keyName, payload) {
      if (method.toUpperCase() === "FORM") {
        this.fetchHelper(url, payload, keyName, postFormData);
      } else if (method.toUpperCase() === "POST") {
        this.fetchHelper(url, payload, keyName, postData);
      } else {
        this.fetchHelper(url, method, keyName, getData);
      }
    }

    componentDidMount() {
      this._isMounted = true;
      // const { payload } = this.props;
      // console.log("componentDidMount", getDisplayName(BaseComponent));
      // if (!R.isEmpty(payload)) this.fetchData(url, payload);
    }

    render() {
      return (
        <BaseComponent
          {...this.state}
          {...this.props}
          setStateData={this.setStateData}
          fetchData={R.curry(this.fetchData)}
        />
      );
    }

    componentWillUnmount() {
      this._isMounted = false;
      // console.log("componentWillUnmounted");
      // console.log("componentDidMount", getDisplayName(BaseComponent));
      if (this._fetchPromise) this._fetchPromise.cancel();
    }
  }

  FetchData.displayName = wrapDisplayName(BaseComponent, "FetchData");
  return FetchData;
};

export const loader = loadMessage => BaseComponent => {
  const Loader = props => {
    if (props.status === fetchEnum.initiate) {
      return (
        <div className="loader">
          <img src={eclipse} className="loader-image" alt="loading ..." />
          <h1 className="loader-message">
            {loadMessage}
          </h1>
        </div>
      );
    } else return <BaseComponent {...props} />;
  };
  Loader.displayName = wrapDisplayName(BaseComponent, "Loader");
  return Loader;
};

export const noop = noopMessage => BaseComponent => {
  const NoOpMessage = props => {
    if (props.status === fetchEnum.noop) {
      return (
        <div className="error">
          <h1 className="error-message">
            {noopMessage}
          </h1>
        </div>
      );
    } else {
      return <BaseComponent {...props} />;
    }
  };
  NoOpMessage.displayName = wrapDisplayName(BaseComponent, "NoOp");
  return NoOpMessage;
};

export const error = () => BaseComponent => {
  const Error = props => {
    if (props.status === fetchEnum.error) {
      return (
        <div className="error">
          <h1 className="error-message">
            {props.errorMessage}
          </h1>
        </div>
      );
    } else {
      return <BaseComponent {...props} />;
    }
  };
  Error.displayName = wrapDisplayName(BaseComponent, "Error");
  return Error;
};

export const Loader = loader("loading..")(<div>testing</div>);
export const Error = error()(<div>Error</div>);
