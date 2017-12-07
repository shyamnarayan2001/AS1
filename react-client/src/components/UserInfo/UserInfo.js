import React from "react";
import userIcon from "../../static/img/AccountIcon.png";
import "./UserInfo.css";

const UserInfo = props => {
  return (
    <div className="user-info">
      <div className="user-avatar">
        <img src={userIcon} alt="User" />
      </div>
      <div className="user-details">
        <h1>{props.isLoggedIn ? props.userName : "Login"}</h1>
        <p>{props.isLoggedIn ? "Logout" : "Login"}</p>
      </div>
    </div>
  );
};

export default UserInfo;
