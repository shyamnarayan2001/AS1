import React from "react";
import "./RunStatus.css";
import "react-datepicker/dist/react-datepicker.css";
import { Container } from "../Container";
import Col from "../../components/Col";
import StatusInfo from "./StatusInfo";
import RunDateInfo from "./RunDateInfo";
import { compose } from "../../utils";
import { fetchData } from "../../hoc/fetchData";
import DateFormat from "dateformat";
import { ViewAnalysis } from "../ViewAnalysis";

export class RunStatus extends React.Component {
  constructor(props) {
    super(props);
    this.state = { showViewAnalysis: false };
    this.tick = this.tick.bind(this);
    // this.openViewAnalysis = this.openViewAnalysis.bind(this,val);
    this.closeViewAnalysis = this.closeViewAnalysis.bind(this);
    this.jsonToArray = this.jsonToArray.bind(this);
  }

  filterNonViewed(data) {
    if (data.viewed === "no") {
      return data;
    }
  }

  jsonToArray(data) {
    var result = [];
    for (var i in data) result.push([i, data[i]]);
    return result;
  }
  compare(a, b) {
    if (a.time > b.time) return -1;
    if (a.time < b.time) return 1;
    return 0;
  }

  tick() {
    this.props.fetchData("get", "/api/runStatus/", "modelStatusData", "get");
  }
  componentDidMount() {
    var self = this;
    setTimeout(function() {
      self.tick(); // do it once and then start it up ...
      self._timer = setInterval(self.tick.bind(self), 1000);
    }, 1000);
  }
  componentWillUnmount() {
    if (this._timer) {
      clearInterval(this._timer);
      this._timer = null;
    }
  }
  openViewAnalysis(val) {
    let name = val.split(",")[0];
    let type = val.split(",")[1];
    const payload = { name: name, runType: type };
    console.log(payload, "payload");
    this.props.fetchData("post", "/api/showGraphs/", "graphData", payload);
    this.setState({ showViewAnalysis: true });
    console.log(name, type);
  }
  closeViewAnalysis() {
    this.setState({ showViewAnalysis: false });
  }
  //.filter(this.filterNonViewed)
  render() {
    return (
      <Container>
        <div style={{ padding: "5px", marginLeft: "25px" }}>
          <Col count={3} style={{ fontWeight: "bold" }}>
            Name/Created At
          </Col>
          <Col count={3} style={{ fontWeight: "bold" }}>
            Type
          </Col>
          <Col count={3} style={{ fontWeight: "bold" }}>
            Status/Action
          </Col>
        </div>
        {this.props.modelStatusData.responseData
          .filter(this.filterNonViewed)
          .sort(this.compare)
          .map((data, index) =>
            <RunStatusItem key={index}>
              <RunStatusBall />
              <RunStatusInfo>
                <Col count={3}>
                  <div>
                    {data.name}
                  </div>
                  <RunDateInfo
                    date={DateFormat(data.time, "dddd, mmmm dS, yyyy")}
                    time={DateFormat(data.time, "h:MM:ss TT")}
                  />
                </Col>
                <Col count="3">
                  <div>
                    {data.runType}
                  </div>
                </Col>
                <Col count={3}>
                  <StatusInfo
                    status={data.status}
                    viewAnalysisClick={this.openViewAnalysis.bind(
                      this,
                      data.name + "," + data.runType
                    )}
                  />
                </Col>
                {/* <Col count="3">
                  <ProgressBar percentage="80" />
                </Col> */}
              </RunStatusInfo>
            </RunStatusItem>
          )}
        <ViewAnalysis
          isOpen={this.state.showViewAnalysis}
          closeViewAnalysis={this.closeViewAnalysis}
          graphData={this.jsonToArray(this.props.graphData.responseData)}
        />
      </Container>
    );
  }
}
export const RunStatusItem = props =>
  <div className="run-status">
    {props.children}
  </div>;

export const RunStatusInfo = props =>
  <div className="run-status-item">
    {props.children}
  </div>;

export const RunStatusBall = () => <div className="run-status-ball" />;

export default compose(
  fetchData(["modelStatusData", "graphData"])
  //createModal(["isOpen", "algoModal"])
)(RunStatus);
