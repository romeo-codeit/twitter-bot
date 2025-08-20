import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createThreadApi } from '../services/api';

function ThreadComposer() {
  const [title, setTitle] = useState('');
  const [tweets, setTweets] = useState(['']); // Start with one empty tweet
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleTweetChange = (index, value) => {
    const newTweets = [...tweets];
    newTweets[index] = value;
    setTweets(newTweets);
  };

  const addTweetInput = () => {
    setTweets([...tweets, '']);
  };

  const removeTweetInput = (index) => {
    if (tweets.length > 1) {
      const newTweets = tweets.filter((_, i) => i !== index);
      setTweets(newTweets);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await createThreadApi({ title, tweets });
      navigate('/dashboard/threads');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create thread.');
    }
  };

  return (
    <div className="bg-gray-800 p-8 rounded-xl shadow-2xl max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Create a New Thread</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-bold text-gray-400 mb-2">Thread Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="e.g., My Thoughts on the New Framework"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-bold text-gray-400 mb-2">Tweets</label>
          <div className="space-y-4">
            {tweets.map((tweet, index) => (
              <div key={index} className="flex items-start space-x-4">
                <span className="text-xl font-bold text-gray-500">{index + 1}</span>
                <textarea
                  value={tweet}
                  onChange={(e) => handleTweetChange(index, e.target.value)}
                  rows="3"
                  className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="What's happening?"
                />
                <button
                  type="button"
                  onClick={() => removeTweetInput(index)}
                  className="p-3 text-red-400 hover:text-red-300 disabled:opacity-50"
                  disabled={tweets.length <= 1}
                >
                  &times;
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-between items-center pt-4">
          <button
            type="button"
            onClick={addTweetInput}
            className="py-2 px-4 bg-gray-600 rounded-lg hover:bg-gray-700"
          >
            Add Another Tweet
          </button>
          <button
            type="submit"
            className="py-3 px-6 font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700"
          >
            Save Thread
          </button>
        </div>
        {error && <p className="mt-4 text-sm text-red-400 text-center">{error}</p>}
      </form>
    </div>
  );
}

export default ThreadComposer;
