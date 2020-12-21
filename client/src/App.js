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
      deidentifedNotesApi: new DeidentifiedNotesApi(new Configuration({basePath: "http://localhost:8080/api/v1"})),
      deidentifiedNote: null
    };
  }

  componentDidMount() {
    let deidentifyRequest = new DeidentifyRequestFromJSON({
      note: {
        text: "Hello, world, my name is May Johnson, and I was born 12 December 1956",
        noteType: "ASDF"
      },
      deidentificationConfigurations: [
        {
          confidenceThreshold: 20,
          deidentificationStrategy: {maskingCharConfig: {}},
          annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
        }
      ]
    });
    this.state.deidentifedNotesApi.createDeidentifiedNotes({deidentifyRequest: deidentifyRequest})
      .then((result) => {alert(JSON.stringify(result))});
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <p>
            {this.state.serviceInfo}
          </p>
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
