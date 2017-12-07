import React, { Component } from "react";
import Menu from "./components/Menu/Menu";
import Header from "./components/Header/Header";
import { UserInfo } from "./components/UserInfo";
import { Route } from "react-router-dom";
import CreateModel from "./sections/CreateModel";
import TestData from "./sections/TestModel";
import PredictModel from "./sections/PredictModel";
import RunStatus from "./sections/RunStatus";
import Models from "./sections/Models";
import Staging from "./sections/Staging";
import MyData from "./sections/MyData";

import "./reset.css";
import "./App.css";

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="group" style={{ height: "23%" }}>
          <Route
            path="/"
            render={() =>
              <Header
                headerItems={[
                  {
                    headerText: "create model",
                    headerDescription: "Evaluate Data to Create New Models",
                    linkPath: "/inputdata"
                  },
                  {
                    headerText: "Test Data",
                    headerDescription: "Test Data against precreated models",
                    linkPath: "/inputdata/testdata"
                  },
                  {
                    headerText: "Predict Data",
                    headerDescription: "Predict data against precreated models",
                    linkPath: "/inputdata/predictdata"
                  }
                ]}
              />}
            exact={true}
          />
          <Route
            path="/inputdata"
            exact={true}
            render={() =>
              <Header
                headerItems={[
                  {
                    headerText: "create model",
                    headerDescription: "Evaluate Data to Create New Models",
                    linkPath: "/inputdata"
                  },
                  {
                    headerText: "Test Data",
                    headerDescription: "Test Data against precreated models",
                    linkPath: "/inputdata/testdata"
                  },
                  {
                    headerText: "Predict Data",
                    headerDescription: "Predict data against precreated models",
                    linkPath: "/inputdata/predictdata"
                  }
                ]}
              />}
          />
          <Route
            path="/inputdata/:headerItem"
            exact={true}
            render={() =>
              <Header
                headerItems={[
                  {
                    headerText: "create model",
                    headerDescription: "Evaluate Data to Create New Models",
                    linkPath: "/inputdata/createmodel"
                  },
                  {
                    headerText: "Test Data",
                    headerDescription: "Test Data against precreated models",
                    linkPath: "/inputdata/testdata"
                  },
                  {
                    headerText: "Predict Data",
                    headerDescription: "Predict data against precreated models",
                    linkPath: "/inputdata/predictdata"
                  }
                ]}
              />}
          />
          <Route
            path="/mydata"
            render={() =>
              <Header
                headerItems={[
                  {
                    headerText: "my data",
                    headerDescription:
                      "Details of Models executed and their status and analysis",
                    linkPath: "/mydata"
                  }
                ]}
              />}
          />
          <Route
            path="/runstatus"
            render={() =>
              <Header
                headerItems={[
                  {
                    headerText: "Run Status",
                    headerDescription:
                      "Details of currently executed models on their existing status and Results",
                    linkPath: "/runstatus"
                  }
                ]}
              />}
          />
          <Route
            path="/models"
            render={() =>
              <Header
                headerItems={[
                  {
                    headerText: "models",
                    headerDescription:
                      "Details of currently created and saved models",
                    linkPath: "/models"
                  }
                ]}
              />}
          />
          <Route
            path="/staging"
            render={() =>
              <Header
                headerItems={[
                  {
                    headerText: "Staging",
                    headerDescription:
                      "Customize table with previous table data by adding to variable with its perspective",
                    linkPath: "/staging"
                  }
                ]}
              />}
          />
          <UserInfo isLoggedIn={true} userName="John Doe" />
        </header>
        <section className="group" style={{ height: "77%" }}>
          <section className="menu-section">
            <Menu
              menuItems={[
                {
                  menuText: "Input Data",
                  menuIcon: "input-data-icon",
                  linkPath: "/inputdata"
                },
                {
                  menuText: "Run status",
                  menuIcon: "run-status-icon",
                  linkPath: "/runstatus"
                },
                {
                  menuText: "my data",
                  menuIcon: "my-data-icon",
                  linkPath: "/mydata"
                },
                {
                  menuText: "models",
                  menuIcon: "models-icon",
                  linkPath: "/models"
                },
                {
                  menuText: "staging",
                  menuIcon: "staging-icon",
                  linkPath: "/staging"
                },
                { menuText: "help", menuIcon: "help-icon", linkPath: "/help" }
              ]}
            />
          </section>
          <section className="container-section">
            <Route path="/" component={CreateModel} exact={true} />
            <Route path="/inputdata" component={CreateModel} exact={true} />
            <Route path="/inputdata/createmodel" component={CreateModel} />
            <Route path="/inputdata/testdata" component={TestData} />
            <Route path="/inputdata/predictdata" component={PredictModel} />
            <Route path="/mydata" component={MyData} exact={true} />
            <Route path="/runstatus" component={RunStatus} exact={true} />
            <Route path="/models" component={Models} exact={true} />
            <Route path="/staging" component={Staging} exact={true} />
          </section>
        </section>
      </div>
    );
  }
}

export default App;
