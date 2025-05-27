import { useState, useEffect } from 'react';

export default function PropertyPanel({ selectedNode, setNodes, result }) {
  const [localId, setLocalId] = useState('');
  const [module, setModule] = useState('');
  const [evaluators, setEvaluators] = useState('');
  const [params, setParams] = useState({});

  useEffect(() => {
    if (selectedNode) {
      setLocalId(selectedNode.id || '');
      setModule(selectedNode.data?.module || '');
      setEvaluators((selectedNode.data?.evaluators || []).join(', '));
      setParams(selectedNode.data?.params || {});
    }
  }, [selectedNode]);

  const updateNode = (field, value) => {
    setNodes((nds) =>
      nds.map((n) =>
        n.id === selectedNode.id
          ? {
            ...n,
            [field === 'id' ? 'id' : 'data']: field === 'id'
              ? value
              : {
                ...n.data,
                [field]: value,
              },
          }
          : n
      )
    );
  };

  const updateParam = (key, value) => {
    const updated = { ...params, [key]: value };
    setParams(updated);
    updateNode('params', updated);
  };

  const handleDelete = () => {
    setNodes((nds) => nds.filter((n) => n.id !== selectedNode.id));
  };

  if (!selectedNode && result) {
    return (
      <div className="w-64 p-4 border-l bg-white text-sm overflow-y-auto">
        <h3 className="text-lg font-semibold mb-4">🧪 실행 결과</h3>
        {Object.entries(result).map(([nodeId, output]) => (
          <div key={nodeId} className="mb-4">
            <div className="font-semibold text-xs mb-1 text-gray-600">🔹 {nodeId}</div>
            <pre className="bg-gray-100 text-xs p-2 rounded whitespace-pre-wrap overflow-auto">
              {typeof output === 'string'
                ? output
                : JSON.stringify(output, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    );
  }

  if (!selectedNode) {
    return (
      <div className="w-64 p-4 border-l bg-white text-sm text-gray-500">
        노드를 선택하세요.
      </div>
    );
  }

  const deleteParam = (keyToDelete) => {
    const updated = { ...params };
    delete updated[keyToDelete];
    setParams(updated);
    updateNode('params', updated);
  };

  return (
    <div className="w-64 p-4 border-l bg-white text-sm overflow-y-auto flex flex-col h-full">
      <h3 className="text-lg font-semibold mb-4 text-gray-700">⚙️ 노드 속성</h3>

      <div className="flex-1 space-y-4">
        {/* ID */}
        <div className="p-2 rounded border bg-blue-50 shadow-sm">
          <label className="block text-xs font-semibold text-blue-700 mb-1">🆔 ID</label>
          <input
            className="w-full border px-2 py-1 text-xs rounded"
            value={localId}
            onChange={(e) => setLocalId(e.target.value)}
            onBlur={() => updateNode('id', localId)}
          />
        </div>

        {/* Type */}
        <div className="p-2 rounded border bg-green-50 shadow-sm">
          <label className="block text-xs font-semibold text-green-700 mb-1">🔧 Type</label>
          <div className="text-xs bg-gray-100 border px-2 py-1 rounded text-gray-800">
            {selectedNode.type}
          </div>
        </div>

        {/* Module */}
        <div className="p-2 rounded border bg-yellow-50 shadow-sm">
          <label className="block text-xs font-semibold text-yellow-700 mb-1">📦 Module</label>
          <input
            className="w-full border px-2 py-1 text-xs rounded"
            value={module}
            onChange={(e) => {
              setModule(e.target.value);
              updateNode('module', e.target.value);
            }}
          />
        </div>

        {/* Params */}
        {selectedNode.type === 'modelNode' && (
          <div className="p-2 rounded border bg-purple-50 shadow-sm">
            <label className="block text-xs font-semibold text-purple-700 mb-2">⚙️ Params</label>
            <div className="space-y-1">
              {Object.entries(params).map(([key, value]) => (
                <div key={key} className="flex items-center gap-1 mb-1">
                  <input
                    className="w-1/3 border text-xs px-1 py-0.5 rounded bg-gray-100"
                    value={key}
                    readOnly
                  />
                  <input
                    className="flex-1 border text-xs px-1 py-0.5 rounded min-w-0"
                    value={value}
                    onChange={(e) => updateParam(key, e.target.value)}
                  />
                  <button
                    onClick={() => deleteParam(key)}
                    className="flex-none text-xs px-2 py-0.5 rounded 
             bg-red-100 text-red-700 hover:bg-red-200 shadow-sm"
                    title="삭제"
                  >
                    ❌
                  </button>

                </div>
              ))}



            </div>
            <AddParam onAdd={(key) => updateParam(key, '')} />
          </div>
        )}

        {/* Evaluators */}
        <div className="p-2 rounded border bg-pink-50 shadow-sm">
          <label className="block text-xs font-semibold text-pink-700 mb-1">📊 Evaluators</label>
          <input
            className="w-full border px-2 py-1 text-xs rounded"
            value={evaluators}
            onChange={(e) => {
              setEvaluators(e.target.value);
              updateNode(
                'evaluators',
                e.target.value.split(',').map((v) => v.trim()).filter(Boolean)
              );
            }}
            placeholder="예: runtime_logger, resource_logger"
          />
        </div>

        {/* Delete button */}
        <div className="mt-6">
          <button
            onClick={handleDelete}
            className="w-full text-xs px-3 py-2 rounded bg-red-500 hover:bg-red-600 text-white font-semibold transition"
          >
            🗑️ 노드 삭제
          </button>
        </div>
      </div>
    </div>
  );

}
function AddParam({ onAdd }) {
  const [newKey, setNewKey] = useState('');

  return (
    <div className="mt-2 flex items-center gap-1 min-w-0">
      <input
        className="flex-1 border text-xs px-2 py-1 rounded bg-white placeholder-gray-400 min-w-0"
        placeholder="새 param 키"
        value={newKey}
        onChange={(e) => setNewKey(e.target.value)}
      />
      <button
        className="flex-none shrink-0 text-xs px-2 py-1 font-medium bg-blue-600 text-white rounded hover:bg-blue-700 shadow-sm"
        onClick={() => {
          if (newKey.trim()) {
            onAdd(newKey.trim());
            setNewKey('');
          }
        }}
      >
        ➕ 추가
      </button>
    </div>
  );
}
