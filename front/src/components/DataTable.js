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
                    setRowData([]); // Fallback to an empty array if data is not as expected
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setRowData([]); // Fallback to an empty array on error
            });
    }, []);



    return (
        <div
            ref={gridRef}
            className="ag-theme-alpine-dark"
            style={{ height: 800, width: 1500 }}
        >
            <AgGridReact
                rowData={rowData}
                columnDefs={columnDefs}
                getRowStyle={getRowStyle}
            />
        </div>
    );
}

export default DataTable;
