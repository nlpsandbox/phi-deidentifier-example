import './App.css';
import { DeidentifiedNotesApi, ToolApi } from '../apis';
import { DeidentifyRequestFromJSON } from '../models';
import React from 'react';
import { Configuration } from '../runtime';
import { DeidentifiedText, deidentificationStates } from './DeidentifiedText';
import { DeidentificationConfigForm } from './DeidentificationConfigForm';
import { encodeString, decodeString } from '../stringSmuggler';
import { AppBar, Box, IconButton, Toolbar, Typography } from '@material-ui/core';
import InfoIcon from '@material-ui/icons/Info';
import { InfoDialog } from './InfoDialog';
import Config from '../config';

const config = new Config()
const apiConfiguration = new Configuration({basePath: config.serverApiUrl()});
const deidentifiedNotesApi = new DeidentifiedNotesApi(apiConfiguration);
const toolApi = new ToolApi(apiConfiguration);

class App extends React.Component {
  constructor(props) {
    super(props);

    // Try loading state from URL
    const { location } = props;
    const queryInUrl = location.pathname.slice(1);
    let deidentifyRequest;
    let showInfo;
    if (queryInUrl) {
      deidentifyRequest = JSON.parse(decodeString(queryInUrl));
      showInfo = false;
    } else {
      deidentifyRequest = {
        deidentificationConfigurations: [{
          key: 0,
          confidenceThreshold: 20,
          deidentificationStrategy: {maskingCharConfig: {maskingChar: "*"}},
          annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
        }],
        note: {
          text: "",
          noteType: "ASDF"  // FIXME: figure out whether and how to get this
        },
        keyMax: 0
      };
      showInfo = true;
    }

    this.state = {
      deidentifiedNoteText: deidentificationStates.EMPTY,
      deidentifyRequest: deidentifyRequest,
      showInfo: showInfo
    };

    this.handleTextAreaChange = this.handleTextAreaChange.bind(this);
  }

  updateUrl = () => {
    const queryInUrl = "/" + encodeString(JSON.stringify(this.state.deidentifyRequest));
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
      annotationTypes: ["text_person_name", "text_physical_address", "text_date"],
      key: this.state.deidentifyRequest.keyMax+1
    };
    deidentificationConfigurations.push(newDeidConfig);
    this.setState(
      {
        deidentifyRequest: {
          ...this.state.deidentifyRequest,
          deidentificationConfigurations: deidentificationConfigurations,
          keyMax: this.state.deidentifyRequest.keyMax + 1
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
      <AppBar style={{ backgroundColor: "grey" }} position="static">
        <Toolbar>
          <Typography variant="h4" style={{ flex: 1 }} >NLP Sandbox PHI Deidentifier</Typography>
          <IconButton onClick={() => {this.setState({showInfo: true})}}><InfoIcon style={{ color: "white" }} /></IconButton>
        </Toolbar>
      </AppBar>
      <div className="left">
        <Box padding={2}>
          <Typography variant="h5" style={{ fontWeight: "bold" }}>Input note:</Typography>
        </Box>
        <textarea onChange={this.handleTextAreaChange} value={this.state.deidentifyRequest.note.text} />
        <br />
        <button className="deidentify-button" onClick={this.deidentifyNote}>De-identify Note</button>
        <br />
        {
          this.state.deidentifyRequest.deidentificationConfigurations.map((deidConfig, index) => 
            <DeidentificationConfigForm
              updateDeidConfig={this.updateDeidentificationConfig}
              deleteDeidConfig={this.deleteDeidConfig}
              key={deidConfig.key}
              index={index}
              {...deidConfig}
            />
          )
        }
        <div className="deid-config-add" onClick={this.addDeidConfig}>&#x002B;</div>
      </div>
      <div className="right">
        <Box padding={2}>
        <Typography variant="h5" style={{ fontWeight: "bold" }}>Deidentified note:</Typography>
        </Box>
        <DeidentifiedText text={this.state.deidentifiedNoteText} />
      </div>
      <InfoDialog
        open={this.state.showInfo}
        handleClose={() => {this.setState({showInfo: false})}}
        toolApi={toolApi}
      />
    </div>
    );
  }
}

export default App;
