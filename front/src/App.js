import React, { useState, useEffect } from 'react';
import DataTable from './components/DataTable';
import './App.css';

function App() {
  const [selectedEndpoint, setSelectedEndpoint] = useState('standart');
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/data/${selectedEndpoint}`);
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    if (selectedEndpoint && !data) {
      fetchData();
    }
  }, [selectedEndpoint, data]);

  const handleButtonClick = (endpoint) => {
    setSelectedEndpoint(endpoint);
    setData(null); // Reset data to trigger a new fetch
  };

  return (
    <div className="App">
      <h1>Data Table with ag-Grid</h1>
      <div className="button-container">
        <button onClick={() => handleButtonClick('standart')}>Standard</button>
        <button onClick={() => handleButtonClick('weapon')}>Weapon</button>
        <button onClick={() => handleButtonClick('event')}>Event</button>
      </div>
      {data && <DataTable data={data} endpoint={selectedEndpoint} />}
    </div>
  );
}

export default App;
