import React, { useState } from "react";
import { Table, TableHead, TableRow, TableCell, TableBody, Typography, Box, TableFooter, TablePagination } from "@mui/material";
import { DataRow } from "./DataRow";

export const DataList = ({ data, header, pagination, refetchDataOnPagination }) => {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);

    const handleChangePage = (e, newPage) => {
        setPage(newPage);
        refetchDataOnPagination(newPage, rowsPerPage);
    };

    const handleChangeRowsPerPage = (e) => {
        setPage(0);
        setRowsPerPage(parseInt(e.target.value, 10));
        refetchDataOnPagination(0, e.target.value);
    };

    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                {header}
            </Typography>
            <Table stickyHeader>
                <TableHead>
                    <TableRow>
                        {Object.keys(data?.rows?.[0] || {}).map((key) => (
                            <TableCell variant="outlined" key={key}>
                                {key}
                            </TableCell>
                        ))}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.rows?.map((row, index) => (
                        <DataRow key={index} rowData={row} />
                    ))}
                </TableBody>
                {pagination && (
                    <TableFooter>
                        <TableRow>
                            <TablePagination
                                rowsPerPageOptions={[5, 10, 25]}
                                count={data.total}
                                rowsPerPage={data.page_size}
                                page={data.page}
                                onPageChange={handleChangePage}
                                onRowsPerPageChange={handleChangeRowsPerPage}
                            />
                        </TableRow>
                    </TableFooter>
                )}
            </Table>
        </Box>
    );
};
