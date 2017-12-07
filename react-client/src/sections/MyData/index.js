import React from "react";
import "./MyData.css";
import DatePicker from "react-datepicker";
import moment from "moment";
import "react-datepicker/dist/react-datepicker.css";
import { Container } from "../Container";
import { TextField } from "../../components/TextBox";
import { DropDown } from "../../components/DropDown";
import Col from "../../components/Col";
import StatusInfo from "../RunStatus/StatusInfo";
import RunDateInfo from "../RunStatus/RunDateInfo";
import { RunStatusItem, RunStatusInfo, RunStatusBall } from "../RunStatus";
import Button from "../../components/Button";
import { compose } from "../../utils";
import { fetchData } from "../../hoc/fetchData";
import DateFormat from "dateformat";
import { ViewAnalysis } from "../ViewAnalysis";

export class MyData extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showViewAnalysis: false,
      modelName: "",
      search: false,
      modelData: [],
      modelType: "",
      fromDate: moment(),
      toDate: moment()
    };
    // this.openViewAnalysis = this.openViewAnalysis.bind(this,val);
    this.closeViewAnalysis = this.closeViewAnalysis.bind(this);
    this.jsonToArray = this.jsonToArray.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.filterViewed = this.filterViewed.bind(this);
    this.handleDateChangeFrom = this.handleDateChangeFrom.bind(this);
    this.handleDateChangeTo = this.handleDateChangeTo.bind(this);

  }

  filterViewed(data) {

    if (this.state.search && this.state.modelName !== "") {
      if (data.viewed === "yes" && (data.name.includes(this.state.modelName) || data.runType === this.state.modelType)) {
        return data;
      }
    }
    else if(this.state.search && this.state.modelName === ""){
       var _date = DateFormat(data.time, "mm, dd, yyyy");
        var date = new Date(_date);
        var dateFrom_to_compare = new Date(this.state.fromDate._d);
        var dateTo_to_compare = new Date(this.state.toDate._d);
       
        if(data.viewed === "yes" && date.getDate() >= dateFrom_to_compare.getDate() && date.getDate() <= dateTo_to_compare.getDate()){
          console.log("filtered data", date,dateFrom_to_compare);
          console.log("filtered data1", date,dateTo_to_compare);
          return data;
        }
    }
    else {
      if (data.viewed === "yes") {
        console.log("initiadata", data);
        return data;
      }
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

  componentDidMount() {
    this.props.fetchData("get", "/api/runStatus/", "myData", "get");
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

  //search
  handleSearch() {
    this.setState({
      search: true
    })
  }

  handleChange(event) {
    const { name, value } = event.target;
    if (name === "model_type") {
      this.setState({
        modelType: value
      })
    }
    if (name === "model_name") {
      this.setState({
        modelName: event.target.value,
        search: false
      })
    }
  }
  handleDateChangeFrom(date) {
    this.setState({
      fromDate: date
    })
  }
  handleDateChangeTo(date) {
    this.setState({
      toDate: date
    })
  }


  render() {
    return (
      <Container>
        <div className="search-form">
          <TextField
            handleChange={this.handleChange}
            value={this.state.modelName}
            labelText="Name of the model"
            name="model_name"
            style={{ display: "inline-block", width: "33%" }}
            inputStyle={{ width: "100%" }}

          />
          <DropDown
            name="model_type"
            value={this.state.modelType}
            labelText="Run Type"
            options={["Training", "Predict", "Test"]}
            style={{ display: "inline-block", width: "33%" }}
            dropDownStyle={{ width: "100%" }}
            handleChange={this.handleChange}
          />
          <div style={{ display: "inline-block", width: "33%" }}>
            <h2 style={{ fontWeight: "bold" }}>Run Date Range</h2>
            <div style={{ display: "inline-block", width: "45%", marginTop: "5px" }}>
              <DatePicker name="from_date" 
                selectsStart 
                selected={this.state.fromDate} 
                startDate={this.state.fromDate}
                endDate={this.state.toDate} 
                onChange={this.handleDateChangeFrom} 
                className="datepicker" 
              />{" "}
            </div>
            <span style={{ fontWeight: "bold", paddingLeft: "5px" }}>to</span>{" "}
            <div style={{ display: "inline-block", width: "45%" }}>
              <DatePicker name="to_date" 
                selectsEnd
                selected={this.state.toDate} 
                startDate={this.state.fromDate}
                endDate={this.state.toDate}  
                onChange={this.handleDateChangeTo} 
                className="datepicker" 
              />
            </div>
          </div>
          <div style={{ padding: "10px" }}>
            <Button
              handleClick={this.handleSearch}
              buttonText="SEARCH"
              style={{ display: "block", width: "40%", margin: "0 auto" }}
            />
          </div>
        </div>
        <div className="run-status-container">
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
          {this.props.myData.responseData
            .filter(this.filterViewed)
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
        </div>
      </Container>
    );
  }
}


export default compose(
  fetchData(["myData", "graphData"])
  //createModal(["isOpen", "algoModal"])
)(MyData);

