import React from 'react';
import { DeidentificationConfigAnnotationTypesEnum } from '../models';
import { IconButton, Box, FormControl, Select, MenuItem, TextField, Grid, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import CloseIcon from '@material-ui/icons/Close';

const styles = (theme) => ({
  maskingCharField: {
    width: "40px",
    textAlign: "center"
  }
});

function TransparentCloseButton(props) {
  return <IconButton disabled color="transparent" size="small" style={{ opacity: "0%" }}><CloseIcon size="small" color="transparent"></CloseIcon></IconButton>;
}

export class DeidentificationConfigForm extends React.Component {
  updateDeidConfig = (newSettings) => {
    this.props.updateDeidConfig(this.props.index, newSettings);
  }

  handleStrategyChange = (event) => {
    // Convert strategy name into correct {key: value} pair
    const newDeidStrategyName = event.target.value;
    let newDeidentificationStrategy = {};
    // FIXME: Ideally this could draw on the models defined in src/models
    if (newDeidStrategyName === "maskingCharConfig") {
      newDeidentificationStrategy[newDeidStrategyName] = { maskingChar: "*" };
    } else {
      newDeidentificationStrategy[newDeidStrategyName] = {}
    }

    // Push up the state
    this.updateDeidConfig({
      deidentificationStrategy: newDeidentificationStrategy
    });
  }

  handleMaskingCharChange = (event) => {
    const maskingChar = event.target.value;
    this.updateDeidConfig({
      deidentificationStrategy: {
        maskingCharConfig: { maskingChar: maskingChar }
      }
    });
  }

  handleConfidenceThresholdChange = (event) => {
    this.updateDeidConfig({
      confidenceThreshold: parseFloat(event.target.value)
    });
  }

  handleAnnotationTypeDelete = (event, index) => {
    const annotationTypes = this.props.annotationTypes
    const newAnnotationTypes = annotationTypes.slice(0, index).concat(annotationTypes.slice(index+1));
    this.updateDeidConfig({
      annotationTypes: newAnnotationTypes
    });
  }

  handleAnnotationTypeAdd = (event) => {
    const annotationType = event.target.value;
    this.updateDeidConfig({
      annotationTypes: this.props.annotationTypes.concat(annotationType)
    });
  }

  handleDelete = () => {
    this.props.deleteDeidConfig(this.props.index);
  }

  getStrategy = () => {
    return Object.keys(this.props.deidentificationStrategy)[0];
  }

  render = () => {
    const { classes } = this.props;
    const allAnnotationTypes = Object.values(DeidentificationConfigAnnotationTypesEnum)
    return (
      <Grid item container direction="column">
        <Grid item>
          <Box bgcolor="primary.main" color="primary.contrastText" padding={2} justify="flex-end">
            <Grid container>
              <Grid item xs={6} align="left">
                <Typography edge="start" variant="h6">De-id Step #{this.props.index + 1}</Typography>
              </Grid>
              <Grid item xs={6} align="right">
                <IconButton onClick={this.handleDelete} color="inherit" size="small"><CloseIcon /></IconButton>
              </Grid>
            </Grid>
          </Box>
        </Grid>
        <Grid item container align="center" spacing={0}>
          <Grid item xs={12} lg={4}>
            <Select label="Method" onChange={this.handleStrategyChange} value={this.getStrategy()}>
              <MenuItem value="maskingCharConfig">Masking Character</MenuItem>
              <MenuItem value="redactConfig">Redact</MenuItem>
              <MenuItem value="annotationTypeConfig">Annotation Type</MenuItem>
            </Select>
            {this.getStrategy() === "maskingCharConfig" &&
              <TextField
                variant="outlined"
                size="small"
                value={this.props.deidentificationStrategy.maskingCharConfig.maskingChar}
                onChange={this.handleMaskingCharChange}
                className={classes.maskingCharField}
                inputProps={{maxLength: 1, style: { textAlign: "center" }}}
              />
            }
          </Grid>
          <Grid item xs={12} lg={4}>
            <TextField label="Confidence Threshold" type="number" onChange={this.handleConfidenceThresholdChange} name="confidenceThreshold" value={this.props.confidenceThreshold} />
          </Grid>
          <Grid item xs={12} lg={4} container direction="column">
            {[...Array(allAnnotationTypes.length)].map((e, index) => {
              const selectWidth = 190;
              if (index < this.props.annotationTypes.length) {
                const annotationType = this.props.annotationTypes[index];
                return (
                  <Grid item>
                    <FormControl style={{ minWidth: selectWidth }}>
                      <Select disabled value={annotationType}><MenuItem value={annotationType}>{annotationType}</MenuItem></Select>
                    </FormControl>
                    <IconButton onClick={(event) => {this.handleAnnotationTypeDelete(event, index);}} size="small"><CloseIcon size="small"/></IconButton>
                  </Grid>
                );
              } else if (index === this.props.annotationTypes.length) {
                return (
                  <Grid item>
                    <FormControl style={{ minWidth: selectWidth }}>
                      <Select value="" displayEmpty onChange={this.handleAnnotationTypeAdd}>
                        <MenuItem value=""><em>Add annotation type</em></MenuItem>
                        {allAnnotationTypes.filter(annotationType => !this.props.annotationTypes.includes(annotationType)).map((annotationType) => {
                          return (
                            <MenuItem value={annotationType}>{annotationType}</MenuItem>
                          );
                        })}
                      </Select>
                    </FormControl>
                    <TransparentCloseButton />
                  </Grid>
                );
              } else {
                return (
                  <Grid item>
                    <FormControl style={{ minWidth: selectWidth }}>
                      <Select disabled value=""><MenuItem value="">...</MenuItem></Select>
                    </FormControl>
                    <TransparentCloseButton />
                  </Grid>
                );
              }
            })}
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

export default withStyles(styles)(DeidentificationConfigForm);
