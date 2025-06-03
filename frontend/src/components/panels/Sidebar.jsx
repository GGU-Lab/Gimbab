const modules = [
  { type: 'inputNode', label: '📥 Input', color: 'bg-blue-100', border: 'border-blue-400' },
  { type: 'modelNode', label: '🧠 Model', color: 'bg-green-100', border: 'border-green-400' },
  { type: 'outputNode', label: '📤 Output', color: 'bg-purple-100', border: 'border-purple-400' },
];

export default function Sidebar({ nodes = [], edges = [], setNodes, setEdges }) {
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
        position: n.position ? { x: n.position.x, y: n.position.y } : { x: 0, y: 0 },
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

  const handleImport = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      try {
        const text = reader.result;
        const data = JSON.parse(text);
        if (!Array.isArray(data.nodes) || !Array.isArray(data.edges)) {
          throw new Error('Invalid structure');
        }

        const importedNodes = data.nodes.map((n) => ({
          id: n.id,
          type: convertNodeTypeToReact(n.type),
          position: n.position && typeof n.position.x === 'number' && typeof n.position.y === 'number'
            ? { x: n.position.x, y: n.position.y }
            : { x: Math.random() * 400 + 100, y: Math.random() * 300 + 100 },
          data: {
            module: n.module || '',
            params: n.params || {},
            evaluators: n.evaluators || [],
          },
        }));

        const importedEdges = data.edges.map((e, idx) => ({
          id: `e-${e.from}-${e.to}-${idx}`,
          source: e.from,
          target: e.to,
          type: 'smoothstep',
        }));

        setNodes(importedNodes);
        setEdges(importedEdges);
      } catch (err) {
        console.error('IMPORT ERROR:', err);
        alert('⚠️ 불러오기 실패: 올바른 JSON 구조인지 확인하세요.');
      }
    };

    reader.readAsText(file);
  };


  return (
    <div className="w-56 h-full p-4 border-r bg-gray-50 shadow-sm flex flex-col justify-between">
      <div>
        <h3 className="text-lg font-semibold mb-4 text-gray-700">📦 모듈 목록</h3>
        <ul className="space-y-3 mb-6">
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

      {/* 하단 버튼 영역 */}
      <div className="flex flex-col gap-2 mt-4">
        <label className="block w-full">
          <input
            type="file"
            accept="application/json"
            className="hidden"
            onChange={handleImport}
          />
          <div className="text-sm px-4 py-2 rounded bg-sky-500 hover:bg-sky-600 text-white text-center font-semibold cursor-pointer transition">
            📥 불러오기
          </div>
        </label>
        <button
          onClick={handleExport}
          style={{
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
    </div>
  );
}

function convertNodeType(type) {
  if (type === 'inputNode') return 'input';
  if (type === 'modelNode') return 'model';
  if (type === 'outputNode') return 'output';
  return 'bridge';
}

function convertNodeTypeToReact(type) {
  if (type === 'input') return 'inputNode';
  if (type === 'model') return 'modelNode';
  if (type === 'output') return 'outputNode';
  return 'bridgeNode';
}
