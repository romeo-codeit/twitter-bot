import React, { useState, useEffect } from 'react';
import {
  getAutoReplySettingsApi,
  setAutoReplySettingsApi,
  getAutoReplyTemplatesApi,
  addAutoReplyTemplateApi,
  deleteAutoReplyTemplateApi
} from '../services/api';

function AutoReplySettings() {
  const [settings, setSettings] = useState({ is_active: false, reply_frequency_minutes: 15 });
  const [templates, setTemplates] = useState([]);
  const [newTemplate, setNewTemplate] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const settingsRes = await getAutoReplySettingsApi();
        const templatesRes = await getAutoReplyTemplatesApi();
        setSettings(settingsRes.data);
        setTemplates(templatesRes.data);
      } catch (error) {
        console.error("Failed to fetch auto-reply data", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSettingsChange = async (e) => {
    const { name, value, type, checked } = e.target;
    const newSettings = { ...settings, [name]: type === 'checkbox' ? checked : parseInt(value) };
    setSettings(newSettings);
    await setAutoReplySettingsApi(newSettings);
  };

  const handleAddTemplate = async (e) => {
    e.preventDefault();
    if (!newTemplate.trim()) return;
    await addAutoReplyTemplateApi({ template_text: newTemplate });
    setNewTemplate('');
    const templatesRes = await getAutoReplyTemplatesApi(); // Refresh templates
    setTemplates(templatesRes.data);
  };

  const handleDeleteTemplate = async (id) => {
    await deleteAutoReplyTemplateApi(id);
    const templatesRes = await getAutoReplyTemplatesApi(); // Refresh templates
    setTemplates(templatesRes.data);
  };

  if (isLoading) return <p className="text-gray-400">Loading settings...</p>;

  return (
    <div className="space-y-12">
      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl">
        <h2 className="text-3xl font-bold mb-2">Auto-Reply Settings</h2>
        <p className="text-gray-400 mb-6">Automatically reply to mentions of your account.</p>
        <div className="space-y-4">
          <div className="flex items-center justify-between bg-gray-700 p-4 rounded-lg">
            <label htmlFor="is_active" className="font-bold text-lg">Enable Auto-Reply</label>
            <input
              type="checkbox"
              id="is_active"
              name="is_active"
              checked={settings.is_active}
              onChange={handleSettingsChange}
              className="w-6 h-6 text-indigo-600 bg-gray-900 border-gray-600 rounded focus:ring-indigo-500"
            />
          </div>
          <div className="flex items-center justify-between bg-gray-700 p-4 rounded-lg">
            <label htmlFor="reply_frequency_minutes" className="font-bold text-lg">Check for mentions every (minutes)</label>
            <input
              type="number"
              id="reply_frequency_minutes"
              name="reply_frequency_minutes"
              value={settings.reply_frequency_minutes}
              onChange={handleSettingsChange}
              className="w-24 p-2 text-gray-200 bg-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              min="5"
              disabled={!settings.is_active}
            />
          </div>
        </div>
      </div>

      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl">
        <h2 className="text-3xl font-bold mb-6">Reply Templates</h2>
        <form onSubmit={handleAddTemplate} className="flex items-center space-x-4 mb-6">
          <input
            type="text"
            value={newTemplate}
            onChange={(e) => setNewTemplate(e.target.value)}
            placeholder="Add a new reply template..."
            className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button type="submit" className="py-3 px-6 font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700">Add</button>
        </form>
        <div className="space-y-3">
          {templates.map(template => (
            <div key={template.id} className="flex justify-between items-center bg-gray-700 p-4 rounded-lg">
              <p className="text-gray-300">{template.template_text}</p>
              <button onClick={() => handleDeleteTemplate(template.id)} className="text-red-400 hover:text-red-300 font-bold">&times;</button>
            </div>
          ))}
          {templates.length === 0 && <p className="text-gray-500 text-center py-4">No templates yet. Add one to get started!</p>}
        </div>
      </div>
    </div>
  );
}

export default AutoReplySettings;
