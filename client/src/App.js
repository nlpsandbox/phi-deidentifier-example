import logo from './logo.svg';
import './App.css';
import { DeidentifiedNotesApi } from './apis';
import { DeidentifyRequestFromJSON } from './models';
import React from 'react';
import { Configuration } from './runtime';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      originalNoteText: "",
      deidentifedNotesApi: new DeidentifiedNotesApi(new Configuration({basePath: "http://localhost:8080/api/v1"})),
      deidentifiedNoteText: "none"
    };
  }

  deidentifyNote() {
    let deidentifyRequest = new DeidentifyRequestFromJSON({
      note: {
        text: this.state.originalNoteText,
        noteType: "ASDF"  // FIXME: figure out whether and how to get this
      },
      deidentificationConfigurations: [  // FIXME: Allow this to be changed
        {
          confidenceThreshold: 20,
          deidentificationStrategy: {maskingCharConfig: {}},
          annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
        }
      ]
    });
    this.state.deidentifedNotesApi.createDeidentifiedNotes({deidentifyRequest: deidentifyRequest})
      .then((deidentifyResponse) => {
        alert(JSON.stringify(deidentifyResponse));
        this.setState({
          deidentifiedNoteText: deidentifyResponse.deidentifiedNote.text
        })
      });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>Input your note here:</p>
          <textarea onChange={(e) => {this.setState({originalNoteText: e.target.value})}} />
          <button onClick={() => {this.deidentifyNote()}}>De-identify Note</button>
          <p>Deidentied note:</p>
          <p>{this.state.deidentifiedNoteText}</p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;
