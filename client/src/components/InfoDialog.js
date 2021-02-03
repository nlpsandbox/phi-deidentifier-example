import React from 'react';
import { Box, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button, Grid, CircularProgress, Link, Paper, Table, TableHead, TableRow, TableCell, TableBody, TableContainer, withStyles } from '@material-ui/core';

export const toolInfoStates = {
  LOADING: 1,
  ERROR: 2
}

const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: "grey",
    color: theme.palette.common.white,
    padding: theme.spacing(1.5)
  },
  body: {
    fontSize: 14,
    padding: theme.spacing(1.5)
  },
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
  root: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

function ToolDependenciesTable(props) {
  let toolDependencies;
  if (props.toolDependencies === toolInfoStates.LOADING) {
    return <Grid item xs={12}><CircularProgress /></Grid>;
  } else if (props.toolDependencies === toolInfoStates.ERROR) {
    return <Grid item xs={12}>API ERROR</Grid>;
  } else {
    return <TableContainer component={Paper}>
    <Table>
      <TableHead>
        <StyledTableRow>
          <StyledTableCell>Type</StyledTableCell>
          <StyledTableCell>Name</StyledTableCell>
          <StyledTableCell>Version</StyledTableCell>
          <StyledTableCell>Author</StyledTableCell>
          <StyledTableCell>Repository</StyledTableCell>
          <StyledTableCell>License</StyledTableCell>
          <StyledTableCell>Description</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {props.toolDependencies.map((toolDependency) => {
          return (
            <StyledTableRow maxHeight="100px">
              <StyledTableCell>{ toolDependency.toolType }</StyledTableCell>
              <StyledTableCell><Link href={ toolDependency.url }>{ toolDependency.name }</Link></StyledTableCell>
              <StyledTableCell>{ toolDependency.version }</StyledTableCell>
              <StyledTableCell><Link href={ "mailto:"+toolDependency.authorEmail }>{ toolDependency.author }</Link></StyledTableCell>
              <StyledTableCell>{ toolDependency.repository }</StyledTableCell>
              <StyledTableCell>{ toolDependency.license }</StyledTableCell>
              <StyledTableCell ><Box style={{ maxHeight: "100%", overflow: "auto" }}>{ toolDependency.description }</Box></StyledTableCell>
            </StyledTableRow>
          );
        })}
      </TableBody>
    </Table>
    </TableContainer>
  }
}

export class InfoDialog extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      toolDependencies: toolInfoStates.LOADING,
      deidentifierInfo: toolInfoStates.LOADING
    };
  }

  componentDidMount = () => {
    // Get tool dependency (i.e. annotator) info from API
    this.props.toolApi.getToolDependencies()
      .then((apiResponse) => {
        this.setState({
          toolDependencies: apiResponse.toolDependencies
        });
      })
      .catch((error) => {
        this.setState({
          toolDependencies: toolInfoStates.ERROR
        });
      });

    // Get deidentifier tool info from API
    this.props.toolApi.getTool()
      .then((apiResponse) => {
        this.setState({
          deidentifierInfo: apiResponse
        })
      })
      .catch(() => {
        this.setState({
          deidentifierInfo: toolInfoStates.ERROR
        })
      });
  }

  render = () => {
    let content;
    if (this.state.deidentifierInfo === toolInfoStates.LOADING) {
      content = <DialogContent><CircularProgress /></DialogContent>
    } else if (this.state.deidentifierInfo === toolInfoStates.ERROR) {
      content = <DialogContent>API Error</DialogContent>;
    } else {
      const toolInfo = this.state.deidentifierInfo;
      content = <DialogContent>
        <DialogContentText id="scroll-dialog-description" tabIndex={-1}>
          You are currently using version <b>{ toolInfo.version }</b> of
          the <Link href={ toolInfo.url }>NLP Sandbox PHI
          Deidentifier</Link>, a tool made for testing the effectiveness of
          community-created, open source PHI annotators submitted to NLP
          Sandbox. You can input a clinical note, which will be annotated and
          de-identified using the following annotators:
        </DialogContentText>
        <ToolDependenciesTable toolDependencies={this.state.toolDependencies} />
      </DialogContent>
    }
    return (
      <Dialog
        open={this.props.open}
        onClose={this.props.handleClose}
        scroll='paper'
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
        maxWidth="lg"
      >
        <DialogTitle id="scroll-dialog-title">About This Tool</DialogTitle>
        {content}
        <DialogActions>
            <Button onClick={this.props.handleClose} color="primary">
              Close
            </Button>
        </DialogActions>
      </Dialog>
    );
  }
}

export default InfoDialog;
