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

    // Try loading state from URL
    const { location } = props;
    const queryInUrl = location.pathname.slice(1);
    let deidentifyRequest;
    if (queryInUrl) {
      deidentifyRequest = JSON.parse(queryInUrl)
    } else {
      deidentifyRequest = {
        deidentificationConfigurations: [{
          confidenceThreshold: 20,
          deidentificationStrategy: {maskingCharConfig: {maskingChar: "*"}},
          annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
        }],
        note: {
          text: "",
          noteType: "ASDF"  // FIXME: figure out whether and how to get this
        }
      }
    }

    this.state = {
      deidentifiedNoteText: deidentificationStates.EMPTY,
      deidentifyRequest: deidentifyRequest
    };

    this.handleTextAreaChange = this.handleTextAreaChange.bind(this);
  }

  updateUrl = () => {
    const queryInUrl = "/" + JSON.stringify(this.state.deidentifyRequest);
    this.props.history.push(queryInUrl);
  }

  deidentifyNote = () => {
    // Mark de-identified text as loading
    this.setState({deidentifiedNoteText: deidentificationStates.LOADING})

    // Build de-identification request
    let deidentifyRequest = new DeidentifyRequestFromJSON(this.state.deidentifyRequest);

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
    let deidentificationConfigurations = [...this.state.deidentifyRequest.deidentificationConfigurations];
    let oldDeidentificationConfig = {...this.state.deidentifyRequest.deidentificationConfigurations[index]}
    deidentificationConfigurations[index] = {
      ...oldDeidentificationConfig,
      ...newSettings
    };
    this.setState(
      {
        deidentifyRequest: {
          ...this.state.deidentifyRequest,
          deidentificationConfigurations: deidentificationConfigurations
        }
      },
      () => this.updateUrl()
    );
  }

  handleTextAreaChange(event) {
    this.setState(
      {
        deidentifyRequest: {
          ...this.state.deidentifyRequest,
          note: {
            ...this.state.deidentifyRequest.note,
            text: event.target.value
          }
        }
      },
      () => this.updateUrl()
    );
  }

  addDeidConfig = (event) => {
    let deidentificationConfigurations = [...this.state.deidentifyRequest.deidentificationConfigurations];
    const newDeidConfig = {
      confidenceThreshold: 20,
      deidentificationStrategy: {maskingCharConfig: {maskingChar: "*"}},
      annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
    };
    deidentificationConfigurations.push(newDeidConfig);
    this.setState(
      {
        deidentifyRequest: {
          ...this.state.deidentifyRequest,
          deidentificationConfigurations: deidentificationConfigurations
        }
      },
      () => this.updateUrl()
    );
  }

  deleteDeidConfig = (index) => {
    let deidentificationConfigurations = [...this.state.deidentifyRequest.deidentificationConfigurations];
    deidentificationConfigurations.splice(index, 1);
    this.setState(
      {
        deidentifyRequest: {
          ...this.state.deidentifyRequest,
          deidentificationConfigurations: deidentificationConfigurations
        }
      },
      () => this.updateUrl()
    );
  }

  render() {
    return (
    <div className="App">
      <div className="left">
        <p>Input note:</p>
        <textarea onChange={this.handleTextAreaChange} value={this.state.deidentifyRequest.note.text} />
        <br />
        <button className="deidentify-button" onClick={this.deidentifyNote}>De-identify Note</button>
        <br />
        {
          this.state.deidentifyRequest.deidentificationConfigurations.map((deidConfig, index) => 
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
