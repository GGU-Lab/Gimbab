import { Handle } from '@xyflow/react';

export default function OutputNode({ id, type, data }) {
  return (
    <div className="p-2 w-44 border border-gray-400 rounded bg-white shadow text-xs relative">
      <Handle type="target" position="left" className="w-2 h-2 bg-green-500 absolute -left-1 top-1/2 -translate-y-1/2" />
      <div className="mb-1 text-[10px] text-gray-400">ID: <strong>{id}</strong></div>
      <div className="font-semibold text-sm">📤 {type}</div>
      <div className="mt-1 text-[11px] text-gray-600 break-all">module: {data.module || '-'}</div>
    </div>
  );
}
