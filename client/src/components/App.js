import { DeidentifiedNotesApi } from '../apis';
import { DeidentifyRequestFromJSON } from '../models';
import React from 'react';
import { Configuration } from '../runtime';
import { DeidentifiedText, deidentificationStates } from './DeidentifiedText';
import { DeidentificationConfigForm } from './DeidentificationConfigForm';
import { withStyles } from '@material-ui/core/styles';
import { Divider, Fab, Grid, Box, TextField, AppBar, Toolbar, Typography } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';
import ClearAllIcon from '@material-ui/icons/ClearAll';

const deidentifiedNotesApi = new DeidentifiedNotesApi(new Configuration({basePath: "http://localhost:8080/api/v1"})) // FIXME: Figure out how to handle hostname

const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  title: {
    display: 'none',
    [theme.breakpoints.up('sm')]: {
      display: 'block',
    },
  },
  container: {
    padding: theme.spacing(2)
  },
  textBox: {
    width: "100%"
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
    <Box className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h4" className={classes.title}>NLP Sandbox PHI Deidentifier</Typography>
        </Toolbar>
      </AppBar>
      <Grid container spacing={2} className={classes.container}>
        <Grid item container direction="column" spacing={2} xs={6} align="center">
          <Grid item>
            <TextField
              multiline
              variant="outlined"
              className={classes.textBox}
              rows={15}
              label="Input Note"
              onChange={this.handleTextAreaChange}
              value={this.state.originalNoteText}
            />
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
          <Fab variant="extended" color="primary" onClick={this.addDeidConfig}>
            <AddIcon /> Add Step
          </Fab>
          </Grid>
        </Grid>
        <Divider orientation="vertical" flexItem />
        <Grid item xs={6}>
          <Typography>Anonymized note:</Typography>
          <DeidentifiedText text={this.state.deidentifiedNoteText} />
          <Fab variant="extended" color="secondary" onClick={this.deidentifyNote}>
            Anonymize <ClearAllIcon />
          </Fab>
        </Grid>
      </Grid>
    </Box>
    );
  }
}

export default withStyles(styles)(App);
