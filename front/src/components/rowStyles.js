// src/components/rowStyles.js

export const getRowStyle = (params) => {
    if (params.data.rank_type === 4) {
        return { background: '#795c42', color: 'white' };
    }

    if (params.data.rank_type === 3) {
        return { background: '#5f4c7b', color: 'white' };
    }

    if (params.data.rank_type === 2) {
        return { background: '#232747', color: 'white' };
    }
    return null;
};
