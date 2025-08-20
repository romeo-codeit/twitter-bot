import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ProtectedRoute from './components/ProtectedRoute';

import TwitterConnect from './components/TwitterConnect';
import ContentQueue from './components/ContentQueue';
import Schedule from './components/Schedule';
import ThreadsPage from './components/ThreadsPage';
import ThreadComposer from './components/ThreadComposer';
import AutoReplySettings from './components/AutoReplySettings';

// --- Placeholder Dashboard Components ---
// In a larger app, these would be in their own files in the `pages` or `components` directory.

function DashboardIndex() {
    return <h2 className="text-2xl text-gray-300">Welcome to your dashboard. Select a section to get started.</h2>
}


function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<LoginPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected Dashboard Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardIndex />} />
        <Route path="twitter" element={<TwitterConnect />} />
        <Route path="content" element={<ContentQueue />} />
        <Route path="schedule" element={<Schedule />} />
        <Route path="threads" element={<ThreadsPage />} />
        <Route path="threads/new" element={<ThreadComposer />} />
        <Route path="threads/:threadId" element={<div className="text-white">Thread Detail Page - To be implemented</div>} />
        <Route path="autoreply" element={<AutoReplySettings />} />
      </Route>
    </Routes>
  );
}

export default App;
