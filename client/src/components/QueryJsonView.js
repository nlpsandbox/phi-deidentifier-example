import { Box, TextField } from "@material-ui/core";

function QueryJsonView(props) {
  return (
    <Box padding={1}>
      <TextField disabled label="Query JSON" variant="filled" multiline rows={15} value={JSON.stringify(props.query, null, 4)} InputProps={{ disableUnderline: true }} fullWidth />
    </Box>
  );
}

export default QueryJsonView;