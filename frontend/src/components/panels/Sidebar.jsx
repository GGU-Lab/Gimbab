const modules = [
  { type: 'inputNode', label: '📥 Input', color: 'bg-blue-100', border: 'border-blue-400' },
  { type: 'modelNode', label: '🧠 Model', color: 'bg-green-100', border: 'border-green-400' },
  { type: 'outputNode', label: '📤 Output', color: 'bg-purple-100', border: 'border-purple-400' },
];

export default function Sidebar({ nodes = [], edges = [] }) {
  const handleDragStart = (event, type) => {
    event.dataTransfer.setData('application/reactflow', type);
    event.dataTransfer.effectAllowed = 'move';
  };

  const handleExport = () => {
    const payload = {
      nodes: nodes.map((n) => ({
        id: n.id,
        type: convertNodeType(n.type),
        module: n.data?.module || '',
        params: n.data?.params || {},
        evaluators: n.data?.evaluators || [],
      })),
      edges: edges.map((e) => ({ from: e.source, to: e.target })),
    };

    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'pipeline_export.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="w-56 h-full p-4 border-r bg-gray-50 shadow-sm flex flex-col justify-between">
      <div>
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

      {/* 📤 내보내기 버튼 */}
      <button
        onClick={handleExport}
        style={{
          marginTop: '1.5rem',
          width: '100%',
          fontSize: '0.875rem', // text-sm
          padding: '0.5rem 1rem', // px-4 py-2
          borderRadius: '0.375rem',
          backgroundColor: '#10b981', // emerald-500
          color: 'white',
          fontWeight: '600',
          transition: 'background-color 0.2s ease-in-out',
          cursor: 'pointer',
        }}
        onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#059669')} // emerald-600
        onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#10b981')}
      >
        📤 내보내기
      </button>

    </div>
  );
}

function convertNodeType(type) {
  if (type === 'inputNode') return 'input';
  if (type === 'modelNode') return 'model';
  if (type === 'outputNode') return 'output';
  return 'bridge';
}
