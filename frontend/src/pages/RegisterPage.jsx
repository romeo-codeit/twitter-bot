import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '../services/api';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    try {
      const response = await registerUser(username, password);
      setSuccess(response.data.message + " Redirecting to login...");
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during registration.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="flex justify-center mb-8">
          <img src="/src/assets/swifter-logo.svg" alt="Swifter Logo" className="w-20 h-20" />
        </div>
        <div className="bg-gray-800 p-8 rounded-xl shadow-2xl">
          <h1 className="text-3xl font-bold text-center mb-2">Create Your Swifter Account</h1>
          <p className="text-gray-400 text-center mb-6">Start automating your Twitter presence.</p>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="username" className="text-sm font-bold text-gray-400 block mb-2">
                Username
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow duration-200"
                required
              />
            </div>
            <div>
              <label htmlFor="password" className="text-sm font-bold text-gray-400 block mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow duration-200"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full py-3 font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-indigo-500 transition-transform transform hover:scale-105"
              disabled={!!success}
            >
              Create Account
            </button>
          </form>
          {error && <p className="mt-4 text-sm text-red-400 text-center">{error}</p>}
          {success && <p className="mt-4 text-sm text-green-400 text-center">{success}</p>}
        </div>
        <p className="text-center text-gray-500 mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-indigo-400 hover:underline">
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
