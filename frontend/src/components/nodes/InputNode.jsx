import { Handle } from '@xyflow/react';

export default function InputNode({ data }) {
  return (
    <div className="p-2 border border-gray-400 rounded bg-white shadow text-sm">
      <div>{data.label}</div>
      <Handle type="source" position="right" />
    </div>
  );
}
