import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button } from '@material-ui/core';


class SaveQueryDialog extends React.Component {
  render = () => {
    return (
      <Dialog
        open={this.props.open}
        onClose={this.props.handleClose}
        aria-labelledby="save-dialog-title"
        aria-describedby="save-dialog-description"
      >
        <DialogTitle id="save-dialog-title">Query JSON</DialogTitle>
        <DialogContent>
          <DialogContentText id="save-dialog-description" style={{ whiteSpace: "pre" }}>
            {JSON.stringify(this.props.deidentificationConfigs, null, 4)}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={this.props.handleClose} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    );
  }
}

export default SaveQueryDialog;