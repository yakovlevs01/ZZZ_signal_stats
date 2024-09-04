import React, { useRef, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.min.css';
import { getRowStyle } from './rowStyles';

function DataTable({ data, endpoint }) {
    const gridRef = useRef(null);

    const columnDefs = useMemo(() => {
        const baseColumns = [
            { field: "id", headerName: "ID" },
            { field: "time", headerName: "Time" },
            { field: "name", headerName: "Name" },
            { field: "rank_type", headerName: "Rank Type" },
            { field: "pity", headerName: "Pity" },
            { field: "item_type", headerName: "Item Type" },
        ];

        return baseColumns;
    }, [endpoint]);

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
                rowData={data ? data.data : []}
                columnDefs={columnDefs}
                getRowStyle={getRowStyle}
                onGridReady={onGridReady}
                onFirstDataRendered={onFirstDataRendered}
            />
        </div>
    );
}

export default DataTable;
