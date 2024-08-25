import React, { useEffect, useState } from 'react';
import { Table } from 'antd';
import axios from 'axios';

const DataTable = () => {
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);

    useEffect(() => {
        axios.get('/data')
            .then(response => {
                const data = response.data;
                setData(data);

                // Генерация заголовков на основе ключей первого объекта
                if (data.length > 0) {
                    const keys = Object.keys(data[0]);
                    const dynamicColumns = keys.map(key => ({
                        title: key,
                        dataIndex: key,
                        key: key,
                        sorter: (a, b) => a[key] > b[key] ? 1 : -1,
                    }));
                    setColumns(dynamicColumns);
                }
            })
            .catch(error => console.error(error));
    }, []);

    return <Table columns={columns} dataSource={data} rowKey={(record) => record.id || record.key} />;
};

export default DataTable;
