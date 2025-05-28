import { Handle } from '@xyflow/react';

export default function InputNode({ id, type, data }) {
  return (
    <div className="p-2 w-44 border border-gray-400 rounded bg-white shadow text-xs relative">
      <Handle type="source" position="right" className="w-2 h-2 bg-blue-500 absolute -right-1 top-1/2 -translate-y-1/2" />
      <div className="mb-1 text-[10px] text-gray-400">ID: <strong>{id}</strong></div>
      <div className="font-semibold text-sm">📥 {type}</div>
      <div className="mt-1 text-[11px] text-gray-600 break-all">module: {data.module || '-'}</div>
    </div>
  );
}
