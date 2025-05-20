import { Handle } from '@xyflow/react';

export default function InputNode({ data }) {
  return (
    <div className="p-2 w-40 h-20 relative border border-gray-400 rounded bg-white shadow text-sm">
      <div>{data.label}</div>
      <Handle
        type="source"
        position="right"
        className="w-3 h-3 bg-blue-500 rounded-full absolute -right-1 top-1/2 -translate-y-1/2"
      />
    </div>
  );
}
