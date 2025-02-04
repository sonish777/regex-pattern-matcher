import React, { useState } from "react";
import {
    Box,
    Button,
    Card,
    CardContent,
    CardHeader,
    FilledInput,
    FormControl,
    FormControlLabel,
    FormGroup,
    FormHelperText,
    Paper,
    TextField
} from "@mui/material";
import { DataList, ExampleData } from "../components";
import { fileService } from "../services";

export const RegexMatchAndReplacer = () => {
    const [file, setFile] = useState(null);
    const [pattern, setPattern] = useState("");
    const [replacement, setReplacement] = useState("");
    const [processedData, setProcessedData] = useState(null);
    const [errors, setErrors] = useState({
        pattern: "",
        replacement: "",
        file: ""
    });
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        const uploadedFile = e.target.files ? e.target.files[0] : null;
        setFile(uploadedFile);
        setErrors((prevErrors) => ({ ...prevErrors, file: "" }));
    };

    const handlePatternChange = (e) => {
        setPattern(e.target.value);
        setErrors((prevErrors) => ({ ...prevErrors, pattern: "" }));
    };

    const handleReplacementChange = (e) => {
        setReplacement(e.target.value);
        setErrors((prevErrors) => ({ ...prevErrors, replacement: "" }));
    };

    const validateInputs = () => {
        let newErrors = {};

        if (!file) newErrors.file = "File is required.";
        if (!pattern.trim()) newErrors.pattern = "Pattern is required.";
        if (!replacement.trim()) newErrors.replacement = "Replacement value is required.";

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleFileUpload = async () => {
        if (!validateInputs()) return;
        setLoading(true);
        try {
            const response = await fileService.uploadFile(file, pattern, replacement);
            const { status, data } = response;
            if (status === "success") {
                setProcessedData(data);
            }
        } catch (error) {
            const { status, errors } = error;
            if (status === "error" && errors) {
                setErrors((prevError) => ({
                    ...prevError,
                    file: errors.file ? errors.file[0] : "",
                    pattern: errors.pattern ? errors.pattern[0] : "",
                    replacement: errors.replacement ? errors.replacement[0] : ""
                }));
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box display="flex" justifyContent="center" padding="20px" columnGap={1} minHeight="100vh">
            <Paper sx={{ padding: 4, boxShadow: 5, width: "40%" }}>
                <Card variant="elevation" sx={{ marginBottom: 3 }}>
                    <CardHeader title="RegXFind&Match" subheader="Upload CSV/Excel file, enter a pattern, and replace it with another value." />
                    <CardContent>
                        <FormGroup>
                            {/* Pattern Description Input */}
                            <FormControl fullWidth margin="dense">
                                <TextField
                                    label="Find Pattern (e.g., 'email addresses')"
                                    value={pattern}
                                    onChange={handlePatternChange}
                                    variant="outlined"
                                    fullWidth
                                    multiline
                                    rows={3}
                                    error={!!errors.pattern}
                                />
                                {errors.pattern && <FormHelperText error>{errors.pattern}</FormHelperText>}
                            </FormControl>

                            {/* Replacement Value Input */}
                            <FormControl fullWidth margin="dense">
                                <TextField
                                    label="Replacement Value"
                                    value={replacement}
                                    onChange={handleReplacementChange}
                                    variant="outlined"
                                    fullWidth
                                    error={!!errors.replacement}
                                />
                                {errors.replacement && <FormHelperText error>{errors.replacement}</FormHelperText>}
                            </FormControl>

                            {/* File Upload Input */}
                            <Box>
                                <FormControl fullWidth margin="dense">
                                    <FormControlLabel
                                        control={<FilledInput type="file" onChange={handleFileChange} />}
                                        label="Upload a CSV/Excel file"
                                        labelPlacement="top"
                                        sx={{ "&.MuiFormControlLabel-root": { alignItems: "start", margin: 0 } }}
                                    />
                                    {errors.file && <FormHelperText error>{errors.file}</FormHelperText>}
                                </FormControl>
                            </Box>
                        </FormGroup>
                        {/* Upload Button */}
                        <Button
                            variant="contained"
                            color="secondary"
                            onClick={handleFileUpload}
                            disabled={loading}
                            loading={loading}
                            sx={{ marginTop: 2 }}
                        >
                            Upload & Process
                        </Button>
                    </CardContent>
                </Card>
            </Paper>
            <Paper sx={{ padding: 4, boxShadow: 5, width: "100%" }}>
                {processedData ? <DataList data={processedData} header="Processed Data" /> : <ExampleData />}
            </Paper>
        </Box>
    );
};
