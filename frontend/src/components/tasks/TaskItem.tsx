import { useState } from "react";

export interface Task {
  id: number;
  title: string;
  description?: string;
  priority: string;
  status: string;
}

interface TaskItemProps {
  task: Task;
  onUpdate: (id: number, data: Partial<Task>) => void;
  onDelete: (id: number) => void;
}

export default function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDesc, setEditDesc] = useState(task.description || "");
  const [editPriority, setEditPriority] = useState(task.priority);

  const isCompleted = task.status === "completed";

  const toggleStatus = () => {
    onUpdate(task.id, {
      status: isCompleted ? "pending" : "completed",
    });
  };

  const handleSave = () => {
    onUpdate(task.id, {
      title: editTitle,
      description: editDesc,
      priority: editPriority,
    });
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="p-4 border-b bg-indigo-50 space-y-3">
        <input
          type="text"
          className="w-full p-2 border rounded text-sm"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          placeholder="Title"
        />
        <textarea
          className="w-full p-2 border rounded text-sm"
          value={editDesc}
          onChange={(e) => setEditDesc(e.target.value)}
          placeholder="Description"
        />
        <div className="flex justify-between items-center">
          <select
            className="p-2 border rounded text-sm"
            value={editPriority}
            onChange={(e) => setEditPriority(e.target.value)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <div className="space-x-2">
            <button onClick={() => setIsEditing(false)} className="text-gray-500 text-sm">Cancel</button>
            <button onClick={handleSave} className="bg-indigo-600 text-white px-3 py-1 rounded text-sm">Save</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`p-4 border-b flex items-center justify-between ${isCompleted ? "bg-gray-50" : "bg-white"}`}>
      <div className="flex items-center space-x-4">
        <input
          type="checkbox"
          checked={isCompleted}
          onChange={toggleStatus}
          className="h-5 w-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 cursor-pointer"
        />
        <div onClick={toggleStatus} className="cursor-pointer">
          <h3 className={`text-lg font-medium ${isCompleted ? "line-through text-gray-400" : "text-gray-900"}`}>
            {task.title}
          </h3>
          {task.description && <p className="text-sm text-gray-500">{task.description}</p>}
        </div>
      </div>
      <div className="flex items-center space-x-3">
        <span className={`px-2 py-1 text-xs font-semibold rounded ${
          task.priority === "high" ? "bg-red-100 text-red-800" :
          task.priority === "medium" ? "bg-yellow-100 text-yellow-800" :
          "bg-green-100 text-green-800"
        }`}>
          {task.priority}
        </span>
        <button
          onClick={() => setIsEditing(true)}
          className="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="text-red-600 hover:text-red-900 text-sm font-medium"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
