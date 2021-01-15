import { DeidentifiedNotesApi } from '../apis';
import { DeidentifyRequestFromJSON } from '../models';
import React from 'react';
import { Configuration } from '../runtime';
import { DeidentifiedText, deidentificationStates } from './DeidentifiedText';
import { DeidentificationConfigForm } from './DeidentificationConfigForm';
import { withStyles } from '@material-ui/core/styles';
import { Button, Grid, Box, TextField, AppBar, Toolbar, Typography } from '@material-ui/core';

const deidentifiedNotesApi = new DeidentifiedNotesApi(new Configuration({basePath: "http://localhost:8080/api/v1"})) // FIXME: Figure out how to handle hostname

const styles = theme => ({
  root: {
    flexGrow: 1,
    fontFamily: 'fixed-width',
  },
  title: {
    display: 'none',
    [theme.breakpoints.up('sm')]: {
      display: 'block',
    },
  }
});

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      originalNoteText: "",
      deidentifiedNoteText: deidentificationStates.EMPTY,
      deidentificationConfigs: [{
        confidenceThreshold: 20,
        deidentificationStrategy: {maskingCharConfig: {maskingChar: "*"}},
        annotationTypes: ["text_person_name", "text_physical_address", "text_date"]
      }]
    };

    this.handleTextAreaChange = this.handleTextAreaChange.bind(this);
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
    this.setState({
      deidentificationConfigs: deidentificationConfigs
    });
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
    this.setState({
      deidentificationConfigs: deidentificationConfigs
    });
  }

  deleteDeidConfig = (index) => {
    let deidentificationConfigs = [...this.state.deidentificationConfigs];
    deidentificationConfigs.splice(index, 1);
    this.setState({
      deidentificationConfigs: deidentificationConfigs
    });
  }

  render() {
    const { classes } = this.props;
    return (
    <React.Fragment className={classes.root}>
    <Box>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h5" className={classes.title}>NLP Sandbox PHI Deidentifier</Typography>
        </Toolbar>
      </AppBar>
      <Grid container maxWidth="80%">
        <Grid item container direction="column" spacing={2} xs={6} align="center">
          <Grid item>
            <TextField
              multiline
              variant="outlined"
              label="Input Note"
              onChange={this.handleTextAreaChange}
              value={this.state.originalNoteText}
            />
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary" onClick={this.deidentifyNote}>De-identify Note</Button>
          </Grid>
            {this.state.deidentificationConfigs.map((deidConfig, index) => 
              <DeidentificationConfigForm
                updateDeidConfig={this.updateDeidentificationConfig}
                deleteDeidConfig={this.deleteDeidConfig}
                key={index}
                index={index}
                {...deidConfig}
              />
            )}
          <Grid item>
            <Button variant="contained" color="secondary" onClick={this.addDeidConfig}>&#x002B;</Button>
          </Grid>
        </Grid>
        <Grid item xs={6}>
          <p>Deidentified note:</p>
          <DeidentifiedText text={this.state.deidentifiedNoteText} />
        </Grid>
      </Grid>
    </Box>
    </React.Fragment>
    );
  }
}

export default withStyles(styles)(App);
