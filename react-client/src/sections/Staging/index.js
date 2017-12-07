import React from "react";
import { Container } from "../Container";
import Col from "../../components/Col";
import CustomizeHeader from "./CustomizeHeader";
import Button from "../../components/Button";
import { TextField } from "../../components/TextBox";
import { DropDown } from "../../components/DropDown";
import { EditTable, EditTableItem, EditTableHeader } from "./EditTable";
import { ColList, ColItem } from "./ColList";
import "./Staging.css";

export default props =>
  <Container>
    <DropDown options={["csv", "excel"]} style={{ padding: "0px" }} labelText="File Type"/>
    <h2 className="staging-desc">
      Customize table with previous table data by adding to variable with its
      perspective
    </h2>
    <div className="staging-main-section">
      <Col count={4} style={{ verticalAlign: "top" }}>
        <ColList>
          {[
            "Column Name 1",
            "Column Name 2",
            "Column Name 3",
            "Column Name 4",
            "Column Name 5"
          ].map((item, index) =>
            <ColItem colName={item} index={index} key={index} />
          )}
        </ColList>
      </Col>
      <Col count={2} style={{ verticalAlign: "top" }}>
        <CustomizeHeader />
      </Col>
      <Col count={4} style={{verticalAlign:'top'}}>
        <EditTable>
          <EditTableHeader header="Current Table" />
          {[
            { colName: "Column Name 1", delete: true, edit: false },
            { colName: "Column Name 2", delete: true, edit: false },
            { colName: "Column Name 3", delete: true, edit: true },
            { colName: "Column Name 4", delete: true, edit: true },
            { colName: "Column Name 5", delete: true, edit: true },
            { colName: "Column Name 6", delete: true, edit: true }
          ].map((item, index) => <EditTableItem {...item} key={index} />)}
        </EditTable>
      </Col>
      <div className="custom-table">
        <TextField labelText="Name of custom table" />
        <div>
          <Button buttonText="SUBMIT" className="custom-table-submit"/>
        </div>
      </div>
    </div>
  </Container>;
