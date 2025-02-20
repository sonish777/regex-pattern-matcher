import React from "react";
import { TableCell, TableRow } from "@mui/material";

export const DataRow = ({ rowData }) => {
    return (
        <TableRow>
            {Object.values(rowData).map((cellValue, index) => (
                <TableCell key={index}>{typeof cellValue != "undefined" ? cellValue.toString() : cellValue}</TableCell>
            ))}
        </TableRow>
    );
};
