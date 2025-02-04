import { Box, FormControl, FormGroup, TextField, Typography } from "@mui/material";
import { DataList } from "./DataList";

const SAMPLE_DATA = {
    raw: [
        { name: "John Doe", email: "john.doe@example.com" },
        { name: "Jane Smith", email: "jane.smith@domain.com" },
        { name: "Alice Brown", email: "alice.brown@website.com" }
    ],
    processed: [
        { name: "John Doe", email: "REDACTED" },
        { name: "Jane Smith", email: "REDACTED" },
        { name: "Alice Brown", email: "REDACTED" }
    ]
};

export const ExampleData = () => {
    return (
        <div>
            <Typography variant="h5">Example Scenario</Typography>
            <Box>
                <FormGroup>
                    <FormControl margin="normal">
                        <TextField
                            label="Find Pattern (e.g., 'email addresses')"
                            disabled
                            multiline
                            rows={3}
                            value="Find email addresses in the Email column"
                        ></TextField>
                    </FormControl>
                    <FormControl margin="normal">
                        <TextField label="Replacement Value" disabled value="REDACTED"></TextField>
                    </FormControl>
                </FormGroup>
            </Box>
            <Box display="flex" gap={5} marginTop={3}>
                <DataList data={SAMPLE_DATA.raw} header="Sample Input Data" />
                <DataList data={SAMPLE_DATA.processed} header="Processed Data" />
            </Box>
        </div>
    );
};
