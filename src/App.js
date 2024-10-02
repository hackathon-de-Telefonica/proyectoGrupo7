import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState([]);

  // Cargar los datos del CSV o desde la API cuando el componente se monte
  useEffect(() => {
    // Si tienes una API, puedes cambiar la URL a la dirección de tu backend.
    // Por ejemplo: axios.get('http://localhost:5000/api/csv')
    axios.get('/path-to-your-csv')
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching the data: ", error);
      });
  }, []);

  return (
    <div className="App">
      <h1>Air Quality Data</h1>
      <table border="1">
        <thead>
          <tr>
            <th>Country</th>
            <th>Air Quality Station</th>
            <th>City</th>
            <th>Pollutant</th>
            <th>Value</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.Country}</td>
              <td>{row['Air Quality Station Name']}</td>
              <td>{row.City}</td>
              <td>{row['Air Pollutant']}</td>
              <td>{row.Value}</td>
              <td>{row['Calculation Time']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
