const BASE_URL = import.meta.env.PROD
  ? 'https://marcy-api.onrender.com'
  : '';

export async function fetchUsers() {
  const res = await fetch(`${BASE_URL}/users`);
  if (!res.ok) throw new Error('Errore nel recupero utenti');
  return res.json();
}

export async function fetchUserEarnings(userId) {
  const res = await fetch(`${BASE_URL}/users/${userId}/earnings`);
  if (!res.ok) throw new Error('Errore nel recupero guadagni');
  return res.json();
}

export async function addEarning({ user_id, amount, currency }) {
  const res = await fetch(`${BASE_URL}/earnings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id, amount, currency }),
  });
  if (!res.ok) throw new Error('Errore nell’aggiunta guadagno');
  return res.json();
}
