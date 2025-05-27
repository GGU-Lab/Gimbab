const modules = [
  { type: 'inputNode', label: '📥 TextInput' },
  { type: 'modelNode', label: '🧠 KcBERT' },
  { type: 'outputNode', label: '📤 JsonOutput' },
];

export default function Sidebar() {
  const handleDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="w-52 p-4 border-r bg-white">
      <h3 className="text-lg font-semibold mb-4">모듈 목록</h3>
      <ul className="space-y-2 text-sm">
        {modules.map((mod) => (
          <li
            key={mod.type}
            className="cursor-move hover:text-blue-600"
            draggable
            onDragStart={(e) => handleDragStart(e, mod.type)}
          >
            {mod.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
