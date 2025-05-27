const modules = [
  { type: 'inputNode', label: '📥 Input', color: 'bg-blue-100', border: 'border-blue-400' },
  { type: 'modelNode', label: '🧠 Model', color: 'bg-green-100', border: 'border-green-400' },
  { type: 'outputNode', label: '📤 Output', color: 'bg-purple-100', border: 'border-purple-400' },
];

export default function Sidebar() {
  const handleDragStart = (event, type) => {
    event.dataTransfer.setData('application/reactflow', type);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="w-56 h-full p-4 border-r bg-gray-50 shadow-sm">
      <h3 className="text-lg font-semibold mb-4 text-gray-700">📦 모듈 목록</h3>
      <ul className="space-y-3">
        {modules.map((mod) => (
          <li
            key={mod.type}
            className={`
              cursor-move select-none px-4 py-2 text-sm rounded border 
              ${mod.color} ${mod.border} 
              hover:bg-opacity-70 hover:shadow-md transition-all
            `}
            draggable
            onDragStart={(e) => handleDragStart(e, mod.type)}
          >
            <span className="font-medium">{mod.label}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
