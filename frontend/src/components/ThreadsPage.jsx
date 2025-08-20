import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getThreadsApi } from '../services/api';

function ThreadsPage() {
  const [threads, setThreads] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchThreads = async () => {
      setIsLoading(true);
      try {
        const response = await getThreadsApi();
        setThreads(response.data);
      } catch (error) {
        console.error("Failed to fetch threads", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchThreads();
  }, []);

  if (isLoading) return <p className="text-gray-400">Loading threads...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Tweet Threads</h1>
        <Link to="/dashboard/threads/new" className="py-2 px-5 font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-transform transform hover:scale-105">
          Create New Thread
        </Link>
      </div>

      <div className="bg-gray-800 rounded-xl shadow-2xl">
        <div className="p-4">
          {threads.length > 0 ? (
            <ul className="space-y-4">
              {threads.map(thread => (
                <li key={thread.id} className="bg-gray-700 p-4 rounded-lg hover:bg-gray-600/50 transition-colors">
                  <Link to={`/dashboard/threads/${thread.id}`} className="block">
                    <h3 className="font-bold text-lg text-indigo-300">{thread.title}</h3>
                    <p className="text-sm text-gray-400">Created: {new Date(thread.created_at).toLocaleDateString()}</p>
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-center text-gray-500 py-8">You haven't created any threads yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ThreadsPage;
