import React from 'react';
import { TextField } from '@material-ui/core';

export const deidentificationStates = {
  EMPTY: 0,
  LOADING: 1,
  ERROR: 2
}

export class DeidentifiedText extends React.Component {
  render() {
    let content;
    if (this.props.text === deidentificationStates.EMPTY) {
      content = "";
    } else if (this.props.text === deidentificationStates.LOADING) {
      content = "Loading...";
    } else if (this.props.text === deidentificationStates.ERROR) {
      content = "API call resulted in error!";
    } else {
      content = this.props.text;
    }

    return <TextField disabled label="Anonymized Note" variant="filled" multiline rows={15} value={content} fullWidth></TextField>;
  }
}

export default DeidentifiedText;