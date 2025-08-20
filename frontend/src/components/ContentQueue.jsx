import React, { useState, useEffect } from 'react';
import { getContentApi, addContentApi, updateContentApi, deleteContentApi } from '../services/api';

const Modal = ({ children, onClose }) => (
  <div className="fixed inset-0 bg-black bg-opacity-70 z-50 flex justify-center items-center p-4 transition-opacity duration-300">
    <div className="bg-gray-800 p-8 rounded-xl shadow-2xl relative w-full max-w-lg transform transition-all duration-300 ease-in-out scale-95 hover:scale-100">
      <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl font-bold">&times;</button>
      {children}
    </div>
  </div>
);

const ContentForm = ({ contentItem, onSave, onCancel }) => {
  const [content, setContent] = useState(contentItem ? contentItem.content : '');
  const [category, setCategory] = useState(contentItem ? contentItem.category : 'general_tech');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...contentItem, content, category });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-2xl font-bold text-white">{contentItem ? 'Edit Content' : 'Add New Content'}</h2>
      <div>
        <label htmlFor="category" className="block text-sm font-bold text-gray-400 mb-2">Category</label>
        <select id="category" value={category} onChange={(e) => setCategory(e.target.value)} className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="general_tech">General Tech</option>
          <option value="tech_tips">Tech Tips</option>
          <option value="my_journey">My Journey</option>
          <option value="tech_stories">Tech Stories</option>
        </select>
      </div>
      <div>
        <label htmlFor="content" className="block text-sm font-bold text-gray-400 mb-2">Tweet Text</label>
        <textarea id="content" value={content} onChange={(e) => setContent(e.target.value)} rows="5" className="w-full p-3 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
      </div>
      <div className="flex justify-end space-x-4 pt-4">
        <button type="button" onClick={onCancel} className="py-2 px-5 bg-gray-600 rounded-lg hover:bg-gray-700 transition-colors">Cancel</button>
        <button type="submit" className="py-2 px-5 bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors">Save Content</button>
      </div>
    </form>
  );
};

function ContentQueue() {
  const [contentList, setContentList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingContent, setEditingContent] = useState(null);

  const fetchContent = async () => {
    setIsLoading(true);
    try {
      const response = await getContentApi();
      setContentList(response.data);
    } catch (error) {
      console.error("Failed to fetch content", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { fetchContent(); }, []);

  const handleSave = async (item) => {
    const apiCall = item.id ? updateContentApi : addContentApi;
    const payload = item.id ? [item.id, { content: item.content, category: item.category }] : [{ content: item.content, category: item.category }];
    await apiCall(...payload);
    fetchContent();
    setIsModalOpen(false);
    setEditingContent(null);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      await deleteContentApi(id);
      fetchContent();
    }
  };

  const openAddModal = () => { setEditingContent(null); setIsModalOpen(true); };
  const openEditModal = (item) => { setEditingContent(item); setIsModalOpen(true); };

  if (isLoading) return <p className="text-gray-400">Loading content queue...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Content Queue</h1>
        <button onClick={openAddModal} className="py-2 px-5 font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-transform transform hover:scale-105">Add Content</button>
      </div>

      <div className="bg-gray-800 rounded-xl shadow-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-700">
              <tr>
                <th className="p-4 text-sm font-semibold text-gray-300 uppercase tracking-wider">Category</th>
                <th className="p-4 text-sm font-semibold text-gray-300 uppercase tracking-wider">Content</th>
                <th className="p-4 text-sm font-semibold text-gray-300 uppercase tracking-wider">Status</th>
                <th className="p-4 text-sm font-semibold text-gray-300 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {contentList.map(item => (
                <tr key={item.id} className="hover:bg-gray-700/50 transition-colors">
                  <td className="p-4 whitespace-nowrap"><span className="px-2 py-1 text-xs font-semibold text-indigo-100 bg-indigo-500/50 rounded-full">{item.category}</span></td>
                  <td className="p-4 max-w-lg text-gray-300 truncate">{item.content}</td>
                  <td className="p-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${item.is_posted ? 'bg-green-500/50 text-green-100' : 'bg-yellow-500/50 text-yellow-100'}`}>
                      {item.is_posted ? 'Posted' : 'Pending'}
                    </span>
                  </td>
                  <td className="p-4 whitespace-nowrap">
                    <button onClick={() => openEditModal(item)} className="text-indigo-400 hover:text-indigo-300 mr-4 font-semibold">Edit</button>
                    <button onClick={() => handleDelete(item.id)} className="text-red-400 hover:text-red-300 font-semibold">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {contentList.length === 0 && <p className="text-center text-gray-500 py-8">Your content queue is empty. Add some content to get started!</p>}
        </div>
      </div>

      {isModalOpen && (
        <Modal onClose={() => setIsModalOpen(false)}>
          <ContentForm contentItem={editingContent} onSave={handleSave} onCancel={() => setIsModalOpen(false)} />
        </Modal>
      )}
    </div>
  );
}

export default ContentQueue;
