import React, { useState } from 'react';
import UploadScreen from './components/UploadScreen';
import DashboardView from './components/DashboardView';

export default function App() {
  const [userSession, setUserSession] = useState(null); // Tracks logged-in user data
  const [dashboardData, setDashboardData] = useState(null);
  const [authMode, setAuthMode] = useState('login'); // 'login' | 'register'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    
    const endpoint = authMode === 'login' ? 'login' : 'register';
    try {
      const response = await fetch(`http://localhost:8000/api/v1/auth/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      
      const resData = await response.json();
      if (!response.ok) throw new Error(resData.detail || 'Authentication execution failure.');
      
      if (authMode === 'login') {
        setUserSession({ id: resData.user_id, token: resData.access_token, name: resData.username });
      } else {
        setMessage('Registration successful! Swapping to secure login panel.');
        setAuthMode('login');
      }
    } catch (err) {
      setMessage(`System Alert: ${err.message}`);
    }
  };

  // State Step 1: User is completely unauthenticated - render authentication forms
  if (!userSession) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6 text-slate-100">
        <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-black uppercase tracking-wider bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              Shield Gate Access
            </h1>
            <p className="text-xs text-slate-500 mt-1">Authenticate node connection credentials</p>
          </div>
          
          <form onSubmit={handleAuthSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Username String</label>
              <input type="text" value={username} onChange={e => setUsername(e.target.value)} required className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm focus:outline-none focus:border-cyan-500 transition-colors" placeholder="vikram_g" />
            </div>
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Secure Password Vector</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} required className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm focus:outline-none focus:border-cyan-500 transition-colors" placeholder="••••••••" />
            </div>
            
            <button type="submit" className="w-full py-2.5 bg-gradient-to-r from-emerald-500 to-cyan-600 font-semibold rounded-xl text-sm hover:opacity-90 transform active:scale-[0.99] transition-all">
              {authMode === 'login' ? 'Log In Secure Link' : 'Register New Core Account'}
            </button>
          </form>

          {message && <p className="mt-4 text-xs text-center text-cyan-400 font-mono">{message}</p>}

          <div className="mt-6 text-center text-xs text-slate-500">
            {authMode === 'login' ? (
              <p>Need access vectors? <span onClick={() => setAuthMode('register')} className="text-cyan-400 cursor-pointer hover:underline">Register an account</span></p>
            ) : (
              <p>Already mapped? <span onClick={() => setAuthMode('login')} className="text-cyan-400 cursor-pointer hover:underline">Return to validation login</span></p>
            )}
          </div>
        </div>
      </div>
    );
  }

  // State Step 2: Authenticated but has no data parsed yet - show upload terminal
  if (dashboardData === null) {
    return <UploadScreen onDataLoaded={(data) => setDashboardData(data)} userSession={userSession} />;
  }

  // State Step 3: Verified session with loaded data arrays - provide full operational dashboard metrics
  return <DashboardView initialData={dashboardData} userSession={userSession} onLogout={() => { setDashboardData(null); setUserSession(null); }} />;
}