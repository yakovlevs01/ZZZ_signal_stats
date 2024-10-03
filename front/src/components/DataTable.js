import React, { useRef, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.min.css';
import { getRowStyle } from './rowStyles';

function DataTable({ data, endpoint }) {
    const gridRef = useRef(null);

    const columnDefs = useMemo(() => {
        const baseColumns = [
            { field: "id", headerName: "ID", floatingFilter: true, filter: true },
            { field: "time", headerName: "Time", floatingFilter: true, filter: true },
            { field: "name", headerName: "Name", floatingFilter: true, filter: true },
            { field: "rank_type", headerName: "Rank Type", floatingFilter: true, filter: 'agSetColumnFilter' },
            { field: "pity", headerName: "Pity", floatingFilter: true, filter: true },
            { field: "item_type", headerName: "Item Type", floatingFilter: true, filter: true },
        ];

        return baseColumns;
    }, [endpoint]);

    const defaultColDef = useMemo(() => ({
        sortable: true,
        resizable: true,
    }), []);

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
                defaultColDef={defaultColDef}
                getRowStyle={getRowStyle}
                onGridReady={onGridReady}
                onFirstDataRendered={onFirstDataRendered}
            />
        </div>
    );
}

export default DataTable;
