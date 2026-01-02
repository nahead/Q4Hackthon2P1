"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/components/providers/AuthProvider";
import { apiClient } from "@/lib/api/client";
import TaskForm from "@/components/tasks/TaskForm";
import TaskItem, { Task } from "@/components/tasks/TaskItem";

export default function DashboardPage() {
  const { user, logout, isLoading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [tasksLoading, setTasksLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem("token");
      const data = await apiClient.get<Task[]>("/tasks", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      setTasks(data);
    } catch (error) {
      console.error("Failed to fetch tasks", error);
    } finally {
      setTasksLoading(false);
    }
  };

  const handleCreateTask = async (taskData: any) => {
    try {
      const token = localStorage.getItem("token");
      const newTask = await apiClient.post<Task>("/tasks", taskData, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      setTasks([newTask, ...tasks]);
    } catch (error) {
      alert("Failed to create task");
    }
  };

  const handleUpdateTask = async (id: number, updateData: Partial<Task>) => {
    try {
      const token = localStorage.getItem("token");
      const updatedTask = await apiClient.put<Task>(`/tasks/${id}`, updateData, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      setTasks(tasks.map(t => t.id === id ? updatedTask : t));
    } catch (error) {
      alert("Failed to update task");
    }
  };

  const handleDeleteTask = async (id: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    try {
      const token = localStorage.getItem("token");
      await apiClient.delete(`/tasks/${id}`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      setTasks(tasks.filter(t => t.id !== id));
    } catch (error) {
      alert("Failed to delete task");
    }
  };

  if (authLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading Auth...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-indigo-600">Evolution of Todo</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700 hidden sm:block">
                Logged in as <span className="font-semibold">{user?.full_name || user?.email}</span>
              </span>
              <button
                onClick={logout}
                className="bg-gray-100 text-gray-700 px-3 py-1.5 rounded-md hover:bg-gray-200 text-sm font-medium transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Create New Task</h2>
            <TaskForm onSubmit={handleCreateTask} />
          </div>

          <div className="md:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-900">Your Tasks</h2>
              <span className="bg-indigo-100 text-indigo-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">
                {tasks.length} total
              </span>
            </div>

            {tasksLoading ? (
              <div className="text-center py-12">Loading tasks...</div>
            ) : tasks.length === 0 ? (
              <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg py-12 text-center">
                <p className="text-gray-500">No tasks yet. Create one to get started!</p>
              </div>
            ) : (
              <div className="bg-white shadow overflow-hidden rounded-md border">
                {tasks.map(task => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onUpdate={handleUpdateTask}
                    onDelete={handleDeleteTask}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
