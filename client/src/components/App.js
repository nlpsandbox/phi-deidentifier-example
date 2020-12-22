import './App.css';
import { DeidentifiedNotesApi } from '../apis';
import { DeidentifyRequestFromJSON } from '../models';
import React from 'react';
import { Configuration } from '../runtime';
import { DeidentifiedText, deidentificationStates } from './DeidentifiedText';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      originalNoteText: "",
      deidentifedNotesApi: new DeidentifiedNotesApi(new Configuration({basePath: "http://localhost:8080/api/v1"})), // FIXME: Figure out how to handle hostname
      deidentifiedNoteText: deidentificationStates.EMPTY
    };
  }

  deidentifyNote() {
    this.setState({deidentifiedNoteText: deidentificationStates.LOADING})
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
        this.setState({
          deidentifiedNoteText: deidentifyResponse.deidentifiedNote.text
        })
      });
  }

  render() {
    let deidentifiedText;
    return (
    <div className="App">
      <div className="left">
        <p>Input note:</p>
        <textarea onChange={(e) => {this.setState({originalNoteText: e.target.value})}} />
        <br />
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
