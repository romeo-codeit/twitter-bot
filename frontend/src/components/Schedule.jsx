import React, { useState, useEffect } from 'react';
import { getScheduleApi, setScheduleApi } from '../services/api';

const PRESET_MODES = {
  'Balanced (3/day)': ['09:00', '15:00', '21:00'],
  'Active (5/day)': ['08:00', '12:00', '16:00', '20:00', '23:00'],
  'Once a day': ['12:00'],
};

function Schedule() {
  const [schedule, setSchedule] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [newTime, setNewTime] = useState('10:00');
  const [error, setError] = useState(null);

  const fetchSchedule = async () => {
    setIsLoading(true);
    try {
      const response = await getScheduleApi();
      setSchedule(response.data.map(item => item.post_time).sort());
    } catch (error) {
      console.error("Failed to fetch schedule", error);
      setError("Could not load your schedule. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { fetchSchedule(); }, []);

  const handleSaveSchedule = async (newSchedule) => {
    try {
      await setScheduleApi(newSchedule);
    } catch (error) {
      console.error("Failed to save schedule", error);
      setError("Could not save your schedule. Please try again.");
      fetchSchedule(); // Revert to last saved state on failure
    }
  };

  const handleAddTime = (e) => {
    e.preventDefault();
    if (newTime && !schedule.includes(newTime)) {
      const updatedSchedule = [...schedule, newTime].sort();
      setSchedule(updatedSchedule);
      handleSaveSchedule(updatedSchedule);
    }
  };

  const handleRemoveTime = (timeToRemove) => {
    const updatedSchedule = schedule.filter(time => time !== timeToRemove);
    setSchedule(updatedSchedule);
    handleSaveSchedule(updatedSchedule);
  };

  const handleSetPreset = (presetTimes) => {
    setSchedule(presetTimes);
    handleSaveSchedule(presetTimes);
  };

  if (isLoading) return <p className="text-gray-400">Loading schedule...</p>;

  return (
    <div className="bg-gray-800 p-8 rounded-xl shadow-2xl max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Your Posting Schedule</h1>
      <p className="text-gray-400 mb-6">Choose a preset or add custom times below. All times are in your local timezone and will be converted to UTC on the server.</p>

      <div className="mb-8 p-4 bg-gray-900/50 rounded-lg">
        <h3 className="text-lg font-semibold mb-3">Preset Modes</h3>
        <div className="flex flex-wrap gap-3">
          {Object.entries(PRESET_MODES).map(([name, times]) => (
            <button key={name} onClick={() => handleSetPreset(times)} className="py-2 px-4 bg-gray-700 rounded-lg hover:bg-indigo-600 transition-colors">
              {name}
            </button>
          ))}
        </div>
      </div>

      <h3 className="text-lg font-semibold mb-3">Custom Time</h3>
      <form onSubmit={handleAddTime} className="flex items-center space-x-4 mb-8">
        <input type="time" value={newTime} onChange={(e) => setNewTime(e.target.value)} className="p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full"/>
        <button type="submit" className="py-3 px-6 font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-transform transform hover:scale-105">Add Time</button>
      </form>

      {error && <p className="text-sm text-red-400 text-center mb-4">{error}</p>}

      <h3 className="text-lg font-semibold mb-3">Current Schedule</h3>
      <div className="space-y-3">
        {schedule.length > 0 ? (
          schedule.map(time => (
            <div key={time} className="flex justify-between items-center bg-gray-700 p-4 rounded-lg transition-all duration-300 hover:bg-gray-600/50">
              <span className="text-lg font-mono tracking-wider">{time}</span>
              <button onClick={() => handleRemoveTime(time)} className="text-red-400 hover:text-red-300 font-bold text-xl">&times;</button>
            </div>
          ))
        ) : (
          <p className="text-gray-500 text-center py-8">No times scheduled yet. Choose a preset or add a custom time to get started!</p>
        )}
      </div>
    </div>
  );
}

export default Schedule;
