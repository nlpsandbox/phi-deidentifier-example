import React from 'react';
import { Box, TextField, Typography } from '@material-ui/core';

export const deidentificationStates = {
  EMPTY: 0,
  LOADING: 1,
  ERROR: 2
}

export class DeidentifiedText extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tabIndex: 0,
    };
  }

  handleTabChange = (event, newValue) => {
    this.setState({
      tabIndex: newValue
    });
  }

  render() {
    let content;
    if (this.props.text === deidentificationStates.EMPTY) {
      content = "Press de-identify note...";
    } else if (this.props.text === deidentificationStates.LOADING) {
      content = "Loading...";
    } else if (this.props.text === deidentificationStates.ERROR) {
      content = "API call resulted in error!";
    } else {
      content = this.props.text;
    }

    return (
      <Box padding={1}>
        <TextField disabled label="Anonymized Note" variant="filled" multiline rows={15} value={content} InputProps={{ disableUnderline: true }} fullWidth />
      </Box>
    );
  }
}

export default DeidentifiedText;