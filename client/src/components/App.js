import './App.css';
import { DeidentifiedNotesApi } from '../apis';
import { DeidentifyRequestFromJSON } from '../models';
import React from 'react';
import { Configuration } from '../runtime';
import { DeidentifiedText, deidentificationStates } from './DeidentifiedText';
import { DeidentificationConfigForm } from './DeidentificationConfigForm';

const deidentifiedNotesApi = new DeidentifiedNotesApi(new Configuration({basePath: "http://localhost:8080/api/v1"})) // FIXME: Figure out how to handle hostname

class App extends React.Component {
  constructor(props) {
    super(props);
    const { location } = props;
    const queryInUrl = location.pathname.slice(1);
    let deidentificationConfigs;
    if (queryInUrl) {
      deidentificationConfigs = JSON.parse(queryInUrl)
    } else {
      deidentificationConfigs = [{
          confidenceThreshold: 20,
          deidentificationStrategy: {maskingCharConfig: {maskingChar: "*"}},
          annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
      }];
    }
    this.state = {
      originalNoteText: "",
      deidentifiedNoteText: deidentificationStates.EMPTY,
      deidentificationConfigs: deidentificationConfigs
    };

    this.handleTextAreaChange = this.handleTextAreaChange.bind(this);
  }

  updateUrl = () => {
    const queryInUrl = "/" + JSON.stringify(this.state.deidentificationConfigs);
    this.props.history.push(queryInUrl);
  }

  deidentifyNote = () => {
    // Mark de-identified text as loading
    this.setState({deidentifiedNoteText: deidentificationStates.LOADING})

    // Build de-identification request
    let deidentificationStrategy = {};
    deidentificationStrategy[this.state.deidentificationStrategy] = {};
    let deidentifyRequest = new DeidentifyRequestFromJSON({
      note: {
        text: this.state.originalNoteText,
        noteType: "ASDF"  // FIXME: figure out whether and how to get this
      },
      deidentificationConfigurations: this.state.deidentificationConfigs
    });

    // Make de-identification request
    deidentifiedNotesApi.createDeidentifiedNotes({deidentifyRequest: deidentifyRequest})
      .then((deidentifyResponse) => {
        this.setState({
          deidentifiedNoteText: deidentifyResponse.deidentifiedNote.text
        });
      })
      .catch(() => {
        this.setState({
          deidentifiedNoteText: deidentificationStates.ERROR
        });
      });
  }

  updateDeidentificationConfig = (index, newSettings) => {
    let deidentificationConfigs = [...this.state.deidentificationConfigs];
    let oldDeidentificationConfig = {...this.state.deidentificationConfigs[index]}
    deidentificationConfigs[index] = {
      ...oldDeidentificationConfig,
      ...newSettings
    };
    this.setState(
      { deidentificationConfigs: deidentificationConfigs },
      () => this.updateUrl()
    );
  }

  handleTextAreaChange(event) {
    this.setState({
      originalNoteText: event.target.value
    });
  }

  addDeidConfig = (event) => {
    let deidentificationConfigs = [...this.state.deidentificationConfigs];
    const newDeidConfig = {
      confidenceThreshold: 20,
      deidentificationStrategy: {maskingCharConfig: {maskingChar: "*"}},
      annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
    };
    deidentificationConfigs.push(newDeidConfig);
    this.setState(
      { deidentificationConfigs: deidentificationConfigs },
      () => this.updateUrl()
    );
  }

  deleteDeidConfig = (index) => {
    let deidentificationConfigs = [...this.state.deidentificationConfigs];
    deidentificationConfigs.splice(index, 1);
    this.setState(
      { deidentificationConfigs: deidentificationConfigs },
      () => this.updateUrl()
    );
  }

  render() {
    return (
    <div className="App">
      <div className="left">
        <p>Input note:</p>
        <textarea onChange={this.handleTextAreaChange} value={this.state.originalNoteText} />
        <br />
        <button className="deidentify-button" onClick={this.deidentifyNote}>De-identify Note</button>
        <br />
        {
          this.state.deidentificationConfigs.map((deidConfig, index) => 
            <DeidentificationConfigForm
              updateDeidConfig={this.updateDeidentificationConfig}
              deleteDeidConfig={this.deleteDeidConfig}
              key={index}
              index={index}
              {...deidConfig}
            />
          )
        }
        <div className="deid-config-add" onClick={this.addDeidConfig}>&#x002B;</div>
      </div>
      <div className="right">
        <p>Deidentified note:</p>
        <DeidentifiedText text={this.state.deidentifiedNoteText} />
      </div>
    </div>
    );
  }
}

export default App;
