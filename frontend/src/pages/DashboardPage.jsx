import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function DashboardPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const navLinks = [
    { path: '/dashboard/twitter', label: 'Twitter Account' },
    { path: '/dashboard/content', label: 'Content Queue' },
    { path: '/dashboard/threads', label: 'Threads' },
    { path: '/dashboard/schedule', label: 'Schedule' },
    { path: '/dashboard/autoreply', label: 'Auto-Reply' },
    // { path: '/dashboard/history', label: 'History' }, // Add when ready
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white flex">
      <aside className="w-64 bg-gray-800 p-6 flex flex-col">
        <div className="flex items-center mb-8">
          <img src="/src/assets/swifter-logo.svg" alt="Swifter Logo" className="w-10 h-10 mr-3" />
          <h1 className="text-2xl font-bold">Swifter</h1>
        </div>
        <nav className="flex-grow">
          <p className="text-sm text-gray-500 font-semibold uppercase mb-4">Your Bot</p>
          <ul>
            {navLinks.map((link) => (
              <li key={link.path} className="mb-2">
                <NavLink
                  to={link.path}
                  className={({ isActive }) =>
                    `block py-2 px-4 rounded transition-colors duration-200 ${
                      isActive ? 'bg-indigo-600' : 'hover:bg-gray-700'
                    }`
                  }
                >
                  {link.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className="mt-auto">
          {user && (
            <div className="text-sm text-gray-400 mb-4">
              Logged in as: <strong>{user.username}</strong>
            </div>
          )}
          <button
            onClick={handleLogout}
            className="w-full py-2 px-4 text-center font-bold bg-red-600 rounded hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </aside>
      <main className="flex-1 p-10">
        <Outlet />
      </main>
    </div>
  );
}

export default DashboardPage;
