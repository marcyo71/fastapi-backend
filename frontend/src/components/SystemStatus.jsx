import React, { useEffect, useState } from 'react';

const BASE_URL = import.meta.env.PROD
  ? 'https://marcy-api.onrender.com'
  : '';

const SystemStatus = () => {
  const [status, setStatus] = useState('⏳ Verifica in corso...');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const res = await fetch(`${BASE_URL}/health`);
        if (res.ok) {
          setStatus('✅ Sistema Online');
        } else {
          setStatus('❌ Sistema Offline');
        }
      } catch (err) {
        setStatus('❌ Errore di connessione');
      }
    };

    checkStatus();
  }, []);

  return (
    <div className="bg-white shadow-md rounded-md p-4 mt-4">
      <h2 className="text-lg font-semibold mb-2">🖥️ Stato Sistema</h2>
      <p>{status}</p>
    </div>
  );
};

export default SystemStatus;
