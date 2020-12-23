import './DeidentificationConfigForm.css'
import React from 'react';

export class DeidentificationConfigForm extends React.Component {
  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  onChange = (event) => {
    this.props.updateDeidStrategy(event.target.value);
  }

  render() {
    return (
      <div className="deid-config-form">
        De-identification strategy: 
        <select onChange={this.onChange}>
          <option value="maskingCharConfig">Masking Character</option>
          <option value="redactConfig">Redact</option>
          <option value="annotationTypeConfig">Annotation Type</option>
        </select>
      </div>
    );
  }
}