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

  handleConfidenceThresholdChange = (event) => {
    this.updateDeidConfig({
      confidenceThreshold: parseFloat(event.target.value)
    });
  }

  handleGenericChange = (event) => {
    const newDeidConfig = {};
    newDeidConfig[event.target.name] = event.target.value;
    this.updateDeidConfig(newDeidConfig);
  }

  handleAnnotationTypeDelete = (event, index) => {
    alert("handleAnnotationTypeDelete called!");
    const annotationTypes = this.props.deidConfig.annotationTypes
    alert(annotationTypes.slice(index))
    const newAnnotationTypes = annotationTypes.slice(0, index).concat(annotationTypes.slice(index+1));
    this.updateDeidConfig({
      annotationTypes: newAnnotationTypes
    });
  }

  render = () => {
    return (
      <div className="deid-config-form">
        De-identification strategy: &nbsp;
        <select onChange={this.handleStrategyChange}>
          <option value="maskingCharConfig">Masking Character</option>
          <option value="redactConfig">Redact</option>
          <option value="annotationTypeConfig">Annotation Type</option>
        </select>
        <br />
        Confidence threshold: &nbsp;
        <input type="number" onChange={this.handleConfidenceThresholdChange} name="confidenceThreshold" />
        <br />
        Annotation types: &nbsp;
        <div>
          {this.props.deidConfig.annotationTypes.map((annotationType, index) => {
            return (
              <div>{annotationType} <button onClick={(event) => {this.handleAnnotationTypeDelete(event, index);}}> - </button></div>
            );
          })}
        </div>
      </div>
    );
  }
}