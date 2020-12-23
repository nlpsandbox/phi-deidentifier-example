import './DeidentificationConfigForm.css'
import React from 'react';

export class DeidentificationConfigForm extends React.Component {
  updateDeidConfig = (newSettings) => {
    this.props.updateDeidConfig(newSettings);
  }

  handleStrategyChange = (event) => {
    // Convert strategy name into correct {key: value} pair
    const newDeidStrategyName = event.target.value;
    let newDeidentificationStrategy = {};
    newDeidentificationStrategy[newDeidStrategyName] = {};

    // Push up the state
    this.updateDeidConfig({
      deidentificationStrategy: newDeidentificationStrategy
    });
  }

  render = () => {
    return (
      <div className="deid-config-form">
        De-identification strategy: 
        <select onChange={this.handleStrategyChange}>
          <option value="maskingCharConfig">Masking Character</option>
          <option value="redactConfig">Redact</option>
          <option value="annotationTypeConfig">Annotation Type</option>
        </select>
      </div>
    );
  }
}