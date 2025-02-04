import React from "react";
import { Table, TableHead, TableRow, TableCell, TableBody, Typography, Box, TableContainer } from "@mui/material";
import { DataRow } from "./DataRow";

export const DataList = ({ data, header }) => {
    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                {header}
            </Typography>
            <Table stickyHeader>
                <TableHead>
                    <TableRow>
                        {Object.keys(data[0]).map((key) => (
                            <TableCell variant="outlined" key={key}>
                                {key}
                            </TableCell>
                        ))}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.map((row, index) => (
                        <DataRow key={index} rowData={row} />
                    ))}
                </TableBody>
            </Table>
        </Box>
    );
};
