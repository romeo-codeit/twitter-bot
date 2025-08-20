import React, { useState, useEffect } from 'react';
import { getTwitterStatusApi, connectTwitterApi } from '../services/api';

const Tooltip = ({ text, children }) => {
  return (
    <div className="relative flex items-center group">
      {children}
      <div className="absolute left-full ml-4 w-48 p-2 bg-gray-600 text-white text-sm rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
        {text}
      </div>
    </div>
  );
};

function TwitterConnect() {
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [keys, setKeys] = useState({
    api_key: '',
    api_secret_key: '',
    access_token: '',
    access_token_secret: '',
  });

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await getTwitterStatusApi();
        setIsConnected(response.data.is_connected);
      } catch (err) {
        setError('Could not verify Twitter connection status.');
      } finally {
        setIsLoading(false);
      }
    };
    checkStatus();
  }, []);

  const handleChange = (e) => {
    setKeys({ ...keys, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    try {
      const response = await connectTwitterApi(keys);
      setSuccess(response.data.message);
      setIsConnected(true);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to connect account.');
    }
  };

  if (isLoading) {
    return <p className="text-gray-400">Loading connection status...</p>;
  }

  if (isConnected) {
    return (
      <div className="bg-gray-800 p-8 rounded-xl shadow-lg text-center transition-all duration-300 ease-in-out">
        <h2 className="text-2xl font-bold text-green-400">Twitter Account Connected</h2>
        <p className="text-gray-400 mt-2">Your account is ready to start posting.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-8 rounded-xl shadow-lg max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-2">Connect Your Twitter/X Account</h2>
      <p className="text-gray-400 mb-6">
        You'll need to provide your own API credentials from the{' '}
        <a href="https://developer.twitter.com/" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:underline">
          Twitter Developer Portal
        </a>.
      </p>
      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.entries(keys).map(([key, value]) => (
          <div key={key}>
            <label htmlFor={key} className="text-sm font-bold text-gray-400 block mb-2">
              <Tooltip text={`Your ${key.replace(/_/g, ' ')} from the developer portal.`}>
                <span className="cursor-help border-b border-dotted border-gray-500">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
              </Tooltip>
            </label>
            <input
              type="password"
              id={key}
              name={key}
              value={value}
              onChange={handleChange}
              className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow duration-200"
              required
            />
          </div>
        ))}
        <button
          type="submit"
          className="w-full py-3 mt-4 font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-indigo-500 transition-transform transform hover:scale-105"
        >
          Connect Account
        </button>
        {error && <p className="mt-4 text-sm text-red-400 text-center">{error}</p>}
        {success && <p className="mt-4 text-sm text-green-400 text-center">{success}</p>}
      </form>
    </div>
  );
}

export default TwitterConnect;
