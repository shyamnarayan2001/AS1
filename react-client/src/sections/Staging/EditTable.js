import React from "react";
import "./EditTable.css";

const EditTable = props =>
  <ul className="edit-table">
    {props.children}
  </ul>;

const EditTableItem = props =>
  <li className="edit-table-item">
    {props.delete ? <span className="local-icon delete-icon" /> : null}
    {props.colName} {props.edit ? <span className="local-icon edit-icon" /> : null}{" "}
  </li>;

const EditTableHeader = props =>
    <li className="edit-table-item edit-table-header">
        {props.header} <span className="local-icon down-arrow"/><span className="local-icon up-arrow"/>
    </li>

export { EditTableItem , EditTable, EditTableHeader}
