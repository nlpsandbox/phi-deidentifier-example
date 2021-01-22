import { DeidentifiedNotesApi } from '../apis';
import { DeidentifyRequestFromJSON } from '../models';
import React from 'react';
import { Configuration } from '../runtime';
import { DeidentifiedText, deidentificationStates } from './DeidentifiedText';
import DeidentificationConfigForm from './DeidentificationConfigForm';
import SaveQueryDialog from './SaveQueryDialog';
import QueryJsonView from './QueryJsonView';
import { withStyles } from '@material-ui/core/styles';
import { Divider, Grid, Box, TextField, AppBar, Toolbar, Typography, ButtonGroup, Button } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';
import ClearAllIcon from '@material-ui/icons/ClearAll';
import { StayPrimaryLandscape } from '@material-ui/icons';

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
      }],
      showSaveQueryDialog: false
    };

    this.handleTextAreaChange = this.handleTextAreaChange.bind(this);
  }

  buildRequest = () => {
    let deidentificationStrategy = {};
    deidentificationStrategy[this.state.deidentificationStrategy] = {};
    const deidentifyRequest = new DeidentifyRequestFromJSON({
      note: {
        text: this.state.originalNoteText,
        noteType: "None"  // FIXME: figure out whether and how to get this
      },
      deidentificationConfigurations: this.state.deidentificationConfigs
    });
    return deidentifyRequest;
  }

  deidentifyNote = () => {
    // Mark de-identified text as loading
    this.setState({deidentifiedNoteText: deidentificationStates.LOADING})

    // Build de-identification request
    const deidentifyRequest = this.buildRequest();

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
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h4" className={classes.title}>NLP Sandbox PHI Deidentifier</Typography>
        </Toolbar>
      </AppBar>
      <Box height="85vh" width="95vw" overflow="auto" padding={2}>
        <Grid container spacing={2} className={classes.container}>
          <Grid item spacing={2} xs={6} align="center">
            <Box padding={1}>
              <TextField
                multiline
                variant="outlined"
                className={classes.textBox}
                rows={15}
                label="Input Note"
                onChange={this.handleTextAreaChange}
                value={this.state.originalNoteText}
              />
            </Box>
            <Box padding={1}>
              <ButtonGroup>
                <Button variant="outlined" color="primary" onClick={this.addDeidConfig}>
                  <AddIcon /> Add Step
                </Button>
                <Button variant="outlined" color="secondary" onClick={this.deidentifyNote}>
                  Anonymize <ClearAllIcon />
                </Button>
              </ButtonGroup>
            </Box>
            <Box maxHeight="40vh" overflow="auto" borderRadius={5} borderColor="primary.main" border={1}>
              {this.state.deidentificationConfigs.map((deidConfig, index) => 
                <DeidentificationConfigForm
                  updateDeidConfig={this.updateDeidentificationConfig}
                  deleteDeidConfig={this.deleteDeidConfig}
                  key={index}
                  index={index}
                  {...deidConfig}
                />
              )}
            </Box>
          </Grid>
          <Divider orientation="vertical" flexItem />
          <Grid item xs={6} container direction="column" spacing={1}>
            <DeidentifiedText text={this.state.deidentifiedNoteText} />
            <QueryJsonView query={this.buildRequest()}/>
          </Grid>
        </Grid>
      </Box>
      <SaveQueryDialog open={this.state.showSaveQueryDialog} handleClose={() => this.setState({showSaveQueryDialog: false})}  deidentificationConfigs={this.state.deidentificationConfigs} />
    </div>
    );
  }
}

export default withStyles(styles)(App);