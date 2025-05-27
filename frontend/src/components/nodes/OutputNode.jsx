import { Handle } from '@xyflow/react';

export default function OutputNode({ data }) {
  return (
    <div className="p-2 w-40 h-20 relative border border-gray-400 rounded bg-white shadow text-sm">
      <Handle
        type="target"
        position="left"
        className="w-3 h-3 bg-green-500 rounded-full absolute -left-1 top-1/2 -translate-y-1/2"
      />
      <div>{data.label}</div>
    </div>
  );
}
