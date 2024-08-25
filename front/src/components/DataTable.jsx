import React, { useEffect, useState } from 'react';
import { Table, Typography, Space } from 'antd';
import axios from 'axios';
import styled from 'styled-components';

const { Title } = Typography;

const StyledTitle = styled(Title)`
    && {
        color: ${({ theme }) => theme.color} !important;
    }
`;



const StyledTable = styled.div`
    .ant-table-thead > tr > th {
        background-color: ${({ theme }) => theme.tableBackground};
        color: ${({ theme }) => theme.color};
    }
    .ant-table-tbody > tr > td {
        background-color: ${({ theme }) => theme.tableBackground};
        color: ${({ theme }) => theme.color};
    }
    .ant-table-tbody > tr.ant-table-row-selected > td {
        background-color: ${({ theme }) => theme.isDarkMode ? '#ffffff' : '#000000'};
        color: ${({ theme }) => theme.isDarkMode ? '#000000' : '#ffffff'};
    }
    .ant-table-tbody > tr.ant-table-row-selected:hover > td {
        background-color: ${({ theme }) => theme.isDarkMode ? '#e6e6e6' : '#333333'};
        color: ${({ theme }) => theme.isDarkMode ? '#000000' : '#ffffff'}; 
    }
    .ant-pagination-item,
    .ant-pagination-item a,
    .ant-pagination-item-active,
    .ant-pagination-item-active a,
    .ant-pagination-prev,
    .ant-pagination-next {
        background-color: ${({ theme }) => theme.tableBackground};
        color: ${({ theme }) => theme.color};
    }
`;





const DataTable = () => {
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [sPity, setSPity] = useState(0);
    const [aPity, setAPity] = useState(0);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/data/standart')
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
            <StyledTitle level={3}>s_pity: {sPity}, a_pity: {aPity}</StyledTitle>
            <StyledTable>
                <Table
                    columns={columns}
                    dataSource={data}
                    rowKey={(record) => record.id || record.key}
                />
            </StyledTable>
        </Space>
    );
};
export default DataTable;
