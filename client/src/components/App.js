import './App.css';
import { DeidentifiedNotesApi } from '../apis';
import { DeidentifyRequestFromJSON } from '../models';
import React from 'react';
import { Configuration } from '../runtime';
import { DeidentifiedText, deidentificationStates } from './DeidentifiedText';
import { DeidentificationConfigForm } from './DeidentificationConfigForm';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      originalNoteText: "",
      deidentifedNotesApi: new DeidentifiedNotesApi(new Configuration({basePath: "http://localhost:8080/api/v1"})), // FIXME: Figure out how to handle hostname
      deidentifiedNoteText: deidentificationStates.EMPTY,
      deidentificationStrategy: "maskingCharConfig"
    };

    this.handleTextAreaChange = this.handleTextAreaChange.bind(this);
    this.handleDeidFormChange = this.handleDeidFormChange.bind(this);
  }

  deidentifyNote() {
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
      deidentificationConfigurations: [  // FIXME: Allow this to be changed
        {
          confidenceThreshold: 20,
          deidentificationStrategy: deidentificationStrategy,
          annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
        }
      ]
    });

    // Make de-identification request
    this.state.deidentifedNotesApi.createDeidentifiedNotes({deidentifyRequest: deidentifyRequest})
      .then((deidentifyResponse) => {
        this.setState({
          deidentifiedNoteText: deidentifyResponse.deidentifiedNote.text
        })
      });
  }

  handleDeidFormChange(deidStrategy) {
    this.setState({
      deidentificationStrategy: deidStrategy
    });
  }

  handleTextAreaChange(event) {
    this.setState({
      originalNoteText: event.target.value
    });
  }

  render() {
    return (
    <div className="App">
      <div className="left">
        <p>Input note:</p>
        <textarea onChange={this.handleTextAreaChange} value={this.state.originalNoteText} />
        <br />
        <DeidentificationConfigForm updateDeidStrategy={this.handleDeidFormChange} deidConfig={this.deidConfig} />
        <button onClick={() => {this.deidentifyNote()}}>De-identify Note</button>
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
