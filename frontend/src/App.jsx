import SystemStatus from './components/SystemStatus';
import UserList from './components/UserList';
import UserForm from './components/UserForm';
import { useState } from 'react';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleUserAdded = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <SystemStatus />
      <UserForm onUserAdded={handleUserAdded} />
      <UserList refreshTrigger={refreshKey} />
    </div>
  );
}

export default App;
<div className="bg-gray-100 min-h-screen p-6">
  <h1 className="text-2xl font-bold text-blue-600 mb-4">Dashboard</h1>
  <SystemStatus />
  <UserForm onUserAdded={handleUserAdded} />
  <UserList refreshTrigger={refreshKey} />
</div>
import EarningsForm from './components/EarningsForm';
import EarningsList from './components/EarningsList';

function App() {
  const [selectedUserId, setSelectedUserId] = useState(1); // esempio

  return (
    <div>
      <h1>Dashboard</h1>
      <EarningsForm userId={selectedUserId} />
      <EarningsList userId={selectedUserId} />
    </div>
  );
}
import UserProfile from './components/UserProfile';

function App() {
  const [selectedUserId, setSelectedUserId] = useState(1); // esempio

  return (
    <div>
      <UserProfile userId={selectedUserId} />
    </div>
  );
}
