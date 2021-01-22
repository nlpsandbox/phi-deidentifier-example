import { Typography } from "@material-ui/core";
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Grid, Button } from '@material-ui/core';

function AnnotatorsInfoDialog(props) {
  return (
    <Dialog
      open={props.open}
      onClose={props.handleClose}
      aria-labelledby="info-dialog-title"
      aria-describedby="info-dialog-description"
    >
      <DialogTitle id="info-dialog-title">About this tool</DialogTitle>
      <DialogContent>
        <DialogContentText id="info-dialog-description">
          <Typography>
            This demo web tool is used to test out PHI annotators built for
            the NLP Sandbox standard. You are currently using the following annotators:
          </Typography>
          <Grid container>
            <Grid item xs={6}>Date annotator:</Grid>
            <Grid item xs={6}>my-date-annotator-123</Grid>
            <Grid item xs={6}>Name annotator: </Grid>
            <Grid item xs={6}>my-name-annotator-456 </Grid>
            <Grid item xs={6}>Address annotator: </Grid>
            <Grid item xs={6}>my-address-annotator-789</Grid>
          </Grid>
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.handleClose} color="primary">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default AnnotatorsInfoDialog;