import React, { useEffect, useState, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.min.css';
import { getRowStyle } from './rowStyles'; // Import the row styles

function DataTable() {
    const [rowData, setRowData] = useState([]);
    const [columnDefs] = useState([
        { field: "id", headerName: "ID" },
        { field: "name", headerName: "Name" },
        { field: "item_type", headerName: "Item Type" },
        { field: "count", headerName: "Count" },
        { field: "rank_type", headerName: "Rank Type" },
        { field: "pity", headerName: "Pity" },
        { field: "time", headerName: "Time" },
        // Add more columns as needed
    ]);

    const gridRef = useRef(null);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/data/standart')
            .then(response => response.json())
            .then(data => {
                if (data && Array.isArray(data.data)) {
                    setRowData(data.data);
                } else {
                    console.error('Data format is incorrect:', data);
                    setRowData([]);
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setRowData([]);
            });
    }, []);

    const onGridReady = (params) => {
        params.api.sizeColumnsToFit();
    };

    const onFirstDataRendered = (params) => {
        params.api.autoSizeAllColumns();
        params.api.setGridOption("domLayout", "print")
    };

    return (
        <div
            ref={gridRef}
            className="ag-theme-alpine-dark"
            style={{ height: 800, width: "" }}
        >
            <AgGridReact
                rowData={rowData}
                columnDefs={columnDefs}
                getRowStyle={getRowStyle}
                onGridReady={onGridReady}
                onFirstDataRendered={onFirstDataRendered}
            />
        </div>
    );
}

export default DataTable;
