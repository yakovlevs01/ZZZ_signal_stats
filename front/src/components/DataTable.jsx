import React, { useEffect, useState } from 'react';
import { Table, Typography, Space } from 'antd';
import axios from 'axios';

const { Title } = Typography;

const DataTable = () => {
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [sPity, setSPity] = useState(0);
    const [aPity, setAPity] = useState(0);

    useEffect(() => {
        axios.get('/data/standart') // Замените 'standart' на нужный тип gacha
            .then(response => {
                const { data, s_pity, a_pity } = response.data;
                setData(data);
                setSPity(s_pity);
                setAPity(a_pity);

                // Генерация заголовков на основе ключей первого объекта
                if (data.length > 0) {
                    const keys = Object.keys(data[0]);
                    const dynamicColumns = keys.map(key => ({
                        title: key,
                        dataIndex: key,
                        key: key,
                        sorter: (a, b) => (a[key] > b[key] ? 1 : -1),
                    }));
                    setColumns(dynamicColumns);
                }
            })
            .catch(error => console.error(error));
    }, []);

    return (
        <Space direction="vertical" style={{ width: '100%' }}>
            <Title level={3}>s_pity: {sPity}, a_pity: {aPity}</Title>
            <Table
                columns={columns}
                dataSource={data}
                rowKey={(record) => record.id || record.key}
            />
        </Space>
    );
};

export default DataTable;
