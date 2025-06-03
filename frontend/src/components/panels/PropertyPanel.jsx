import { useState, useEffect } from 'react';

export default function PropertyPanel({ selectedNode, setNodes, result, setSelected }) {
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
    if (typeof window !== 'undefined' && typeof setSelected === 'function') setSelected(null);
  };

  if (!selectedNode && result) {
    const handleExportResult = () => {
      const blob = new Blob([JSON.stringify(result, null, 2)], {
        type: 'application/json',
      });
      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = 'result_export.json';
      a.click();

      URL.revokeObjectURL(url);
    };

    return (
      <div className="w-64 p-4 border-l bg-white text-sm overflow-y-auto flex flex-col h-full">
        <h3 className="text-lg font-semibold mb-4 text-gray-700">🧪 실행 결과</h3>

        <div className="flex-1 space-y-4 overflow-y-auto">
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

        {/* 📤 결과 내보내기 버튼 */}
        <button
          onClick={handleExportResult}
          className="mt-4 w-full text-xs px-3 py-2 rounded-md bg-emerald-500 text-white font-semibold hover:bg-emerald-600 transition-colors"
        >
          📤 결과 내보내기
        </button>
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
        <div className="p-2 rounded border bg-purple-50 shadow-sm">
          <label className="block text-xs font-semibold text-purple-700 mb-2">⚙️ Params</label>
          <div className="space-y-1">
            {Object.entries(params).map(([key, value]) => (
              <div key={key} className="flex items-center gap-1 mb-1 bg-purple-50 rounded px-1 py-1">
                <input
                  className="w-1/3 border text-xs px-1 py-2 rounded bg-gray-100"
                  value={key}
                  readOnly
                />
                <input
                  className="flex-1 border text-xs px-1 py-2 rounded min-w-0"
                  value={value}
                  onChange={(e) => updateParam(key, e.target.value)}
                />
                <button
                  onClick={() => deleteParam(key)}
                  title="삭제"
                  className="h-8 w-8 flex items-center justify-center text-lg rounded bg-red-500 text-white font-bold shadow-sm hover:bg-red-700 transition-colors"
                >
                  ❌
                </button>
              </div>
            ))}
          </div>
          <AddParam onAdd={(key) => updateParam(key, '')} />
        </div>

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
      </div>

      <div className="mt-auto">
        <button
          onClick={handleDelete}
          className="w-full text-base px-3 py-2 rounded-md bg-red-500 text-white font-extrabold hover:bg-red-700 transition-colors"
        >
          🗑️ <span className="font-extrabold">노드 삭제</span>
        </button>
      </div>
    </div>
  );
}

function AddParam({ onAdd }) {
  const [newKey, setNewKey] = useState('');

  return (
    <div className="mt-2 flex gap-2 items-center min-w-0 bg-blue-50 rounded px-1 py-1">
      <input
        placeholder="새 param 키"
        value={newKey}
        onChange={(e) => setNewKey(e.target.value)}
        className="flex-1 text-xs px-2 py-2 rounded border border-gray-300 bg-white min-w-0 text-gray-900"
      />
      <button
        onClick={() => {
          if (newKey.trim()) {
            onAdd(newKey.trim());
            setNewKey('');
          }
        }}
        className="h-8 px-4 flex items-center justify-center text-sm rounded font-semibold bg-blue-600 text-white shadow-sm hover:bg-blue-800 transition-colors"
      >
        ➕ 추가
      </button>
    </div>

  );
}
