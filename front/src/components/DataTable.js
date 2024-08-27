import React, { useEffect, useState, useRef } from 'react';

import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.min.css';

function DataTable() {
    const [rowData, setRowData] = useState([]);
    const [columnDefs] = useState([
        { headerName: "ID", field: "id" },
        { headerName: "Name", field: "name" },
        { headerName: "Item Type", field: "item_type" },
        { headerName: "Count", field: "count" },
        { headerName: "Rank Type", field: "rank_type" },
        { headerName: "Pity", field: "pity" },
        { headerName: "Time", field: "time" },
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
            style={{ height: 800, width: 1700 }}
        >
            <AgGridReact
                rowData={rowData}
                columnDefs={columnDefs}>
            </AgGridReact>
        </div>
    );
}

export default DataTable;
