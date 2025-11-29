import React, { useEffect, useState } from 'react';

const SystemStatus = () => {
  const [statusData, setStatusData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/status')
      .then((res) => {
        if (!res.ok) throw new Error('Errore nel recupero dello stato');
        return res.json();
      })
      .then((data) => setStatusData(data))
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <div>Errore: {error}</div>;
  if (!statusData) return <div>Caricamento stato sistema...</div>;

  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px' }}>
      <h2>🖥️ Stato Backend</h2>
      <ul>
        <li><strong>Status:</strong> {statusData.status}</li>
        <li><strong>Debug:</strong> {statusData.debug}</li>
        <li><strong>Ambiente:</strong> {statusData.env}</li>
        <li><strong>Uptime:</strong> {statusData.uptime}</li>
      </ul>
    </div>
  );
};

export default SystemStatus;
