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
          style={{
            marginTop: '1rem',
            width: '100%',
            fontSize: '0.75rem', // text-xs
            padding: '0.5rem 0.75rem', // px-3 py-2
            borderRadius: '0.375rem',
            backgroundColor: '#10b981',
            color: 'white',
            fontWeight: '600',
            transition: 'background-color 0.2s ease-in-out',
            cursor: 'pointer',
          }}
          onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#059669')}
          onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#10b981')}
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
                    title="삭제"
                    style={{
                      fontSize: '12px',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      backgroundColor: '#fee2e2',   // red-100
                      color: '#b91c1c',             // red-700
                      boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
                      cursor: 'pointer',
                      border: 'none',
                    }}
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
            style={{
              width: '100%',
              fontSize: '12px',
              padding: '8px 12px',
              borderRadius: '6px',
              backgroundColor: '#ef4444', // red-500
              color: 'white',
              fontWeight: 600,
              border: 'none',
              cursor: 'pointer',
              transition: 'background-color 0.2s ease-in-out',
            }}
            onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#dc2626')} // red-600
            onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#ef4444')}
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
    <div style={{ marginTop: '8px', display: 'flex', gap: '6px', alignItems: 'center', minWidth: 0 }}>
      <input
        placeholder="새 param 키"
        value={newKey}
        onChange={(e) => setNewKey(e.target.value)}
        style={{
          flex: 1,
          fontSize: '12px',
          padding: '6px 8px',
          borderRadius: '4px',
          border: '1px solid #d1d5db', // gray-300
          backgroundColor: '#ffffff',
          minWidth: 0,
          color: '#111827',
        }}
      />
      <button
        onClick={() => {
          if (newKey.trim()) {
            onAdd(newKey.trim());
            setNewKey('');
          }
        }}
        style={{
          fontSize: '12px',
          padding: '6px 10px',
          borderRadius: '4px',
          fontWeight: 500,
          backgroundColor: '#2563eb', // blue-600
          color: '#ffffff',
          border: 'none',
          cursor: 'pointer',
          boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
        }}
      >
        ➕ 추가
      </button>
    </div>

  );
}
