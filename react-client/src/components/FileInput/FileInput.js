import React from 'react';
import './FileInput.css';

const FileInput = (props) => (
        <label className="fileinput" style={props.style}>
            {props.labelText}
            <input type="file" accept=".csv,.xls,.xlsx, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" name={props.name} onChange={(event) => props.handleChange(event)} />
        </label>
)

export default FileInput;
