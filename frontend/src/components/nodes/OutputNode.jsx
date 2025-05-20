import { Handle } from '@xyflow/react';

export default function OutputNode({ data }) {
  return (
    <div className="p-2 border border-gray-400 rounded bg-white shadow text-sm">
      <Handle type="target" position="left" />
      <div>{data.label}</div>
    </div>
  );
}
