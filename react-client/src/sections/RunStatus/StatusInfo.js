import React from "react";
import Button from "../../components/Button";
import "./StatusInfo.css";

const StatusInfo = props =>
  <div className="status-info">
    <h3 className="font-bold">
      {props.modelName}
    </h3>
    <div
      className={
        props.status === "Success"
          ? "completed-progress-section"
          : "progress-section"
      }
    >
      <div className="col-1-2">
        {props.status === "Success"
          ? <Button
              buttonText="RE RUN"
              hover={false}
              className="status-button blue"
            />
          : <span className={props.status === "Success"
            ? "status-msg"
            :"error-msg"
          }>{props.status}</span>}
      </div>
      <div className="col-1-2">
        {props.status === "Success"
          ? <Button
              buttonText="VIEW ANALYSIS"
              hover={false}
              className="status-button green"
              handleClick = {props.viewAnalysisClick}
            />
          :<Button
              buttonText="Delete"
              hover={false}
              className="status-button stop"
            />
          }
          {props.status === "Running"
            ?<Button
              buttonText="STOP RUN"
              hover={false}
              className="status-button stop"
            />
            :<span className="status-msg"></span>
          }
      </div>
    </div>
  </div>;

export default StatusInfo;
