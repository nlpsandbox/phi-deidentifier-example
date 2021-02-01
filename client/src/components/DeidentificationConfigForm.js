import './DeidentificationConfigForm.css'
import React from 'react';
import { DeidentificationConfigAnnotationTypesEnum } from '../models';
import { Collapse } from '@material-ui/core';

export class DeidentificationConfigForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      expand: false
    }
  }

  updateDeidConfig = (newSettings) => {
    this.props.updateDeidConfig(this.props.index, newSettings);
  }

  handleStrategyChange = (event) => {
    // Convert strategy name into correct {key: value} pair
    const newDeidStrategyName = event.target.value;
    let newDeidentificationStrategy = {};
    // FIXME: Ideally this could draw on the models defined in src/models
    if (newDeidStrategyName === "maskingCharConfig") {
      newDeidentificationStrategy[newDeidStrategyName] = { maskingChar: "*" };
    } else {
      newDeidentificationStrategy[newDeidStrategyName] = {}
    }

    // Push up the state
    this.updateDeidConfig({
      deidentificationStrategy: newDeidentificationStrategy
    });
  }

  handleMaskingCharChange = (event) => {
    const maskingChar = event.target.value;
    this.updateDeidConfig({
      deidentificationStrategy: {
        maskingCharConfig: { maskingChar: maskingChar }
      }
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
    this.setState(
      { expand: false }, () => {
        setTimeout(
          () => {this.props.deleteDeidConfig(this.props.index);},
          250
        )
      }
    );
  }

  componentDidMount = () => {
    this.setState({ expand: true });
  }

  getStrategy = () => {
    return Object.keys(this.props.deidentificationStrategy)[0];
  }

  render = () => {
    const allAnnotationTypes = Object.values(DeidentificationConfigAnnotationTypesEnum)
    return (
      <Collapse in={this.state.expand}>
      <div className="deid-config-form">
        <div className="deid-config-form-bar">
          <div className="deid-config-header">De-id Step #{this.props.index + 1}</div>
          <div className="deid-config-remove" onClick={this.handleDelete}></div>
        </div>
        <table>
          <tr>
            <td>
              Method
            </td>
            <td>
              <select onChange={this.handleStrategyChange} value={this.getStrategy()}>
                <option value="maskingCharConfig">Masking Character</option>
                <option value="redactConfig">Redact</option>
                <option value="annotationTypeConfig">Annotation Type</option>
              </select>
              &nbsp;
              {this.getStrategy() === "maskingCharConfig" &&
                <input type="text" maxLength={1} value={this.props.deidentificationStrategy.maskingCharConfig.maskingChar} onChange={this.handleMaskingCharChange} />
              }
            </td>
          </tr>
          <tr>
            <td>
              Confidence threshold
            </td>
            <td>
              <input type="number" onChange={this.handleConfidenceThresholdChange} name="confidenceThreshold" value={this.props.confidenceThreshold} />
            </td>
          </tr>
          <tr>
          <td>
            Annotation types
          </td>
          <td>
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
            </td>
          </tr>
        </table>
      </div>
      </Collapse>
    );
  }
}