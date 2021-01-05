import './DeidentificationConfigForm.css'
import React from 'react';
import { DeidentificationConfigAnnotationTypesEnum, DeidentificationConfigDeidentificationStrategy } from '../models';

export class DeidentificationConfigForm extends React.Component {
  updateDeidConfig = (newSettings) => {
    this.props.updateDeidConfig(this.props.index, newSettings);
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

  handleAnnotationTypeDelete = (event, index) => {
    const annotationTypes = this.props.annotationTypes
    const newAnnotationTypes = annotationTypes.slice(0, index).concat(annotationTypes.slice(index+1));
    this.updateDeidConfig({
      annotationTypes: newAnnotationTypes
    });
  }

  handleAnnotationTypeAdd = (event) => {
    const annotationType = event.target.value;
    this.updateDeidConfig({
      annotationTypes: this.props.annotationTypes.concat(annotationType)
    });
  }

  handleDelete = () => {
    this.props.deleteDeidConfig(this.props.index);
  }

  render = () => {
    const allAnnotationTypes = Object.values(DeidentificationConfigAnnotationTypesEnum)
    return (
      <div className="deid-config-form">
        <div className="deid-config-form-bar">
          <div className="deid-config-header">De-identification Configuration #{this.props.index + 1}</div>
          <div className="deid-config-remove" onClick={this.handleDelete}></div>
        </div>
        De-identification strategy: &nbsp;
        <select onChange={this.handleStrategyChange} value={Object.keys(this.props.deidentificationStrategy)[0]}>
          <option value="maskingCharConfig">Masking Character</option>
          <option value="redactConfig">Redact</option>
          <option value="annotationTypeConfig">Annotation Type</option>
        </select>
        <br />
        Confidence threshold: &nbsp;
        <input type="number" onChange={this.handleConfidenceThresholdChange} name="confidenceThreshold" value={this.props.confidenceThreshold} />
        <br />
        Annotation types: &nbsp;
        <div>
          {this.props.annotationTypes.map((annotationType, index) => {
            return (
              <div>{annotationType} <button onClick={(event) => {this.handleAnnotationTypeDelete(event, index);}}> - </button></div>
            );
          })}
          {this.props.annotationTypes.length < allAnnotationTypes.length &&
            <select value="" onChange={this.handleAnnotationTypeAdd}>
              <option value="">...</option>
              {allAnnotationTypes.filter(annotationType => !this.props.annotationTypes.includes(annotationType)).map((annotationType) => {
                return (
                  <option value={annotationType}>{annotationType}</option>
                );
              })}
            </select>
          }
        </div>
      </div>
    );
  }
}