import React from "react";
import { Handle } from "@xyflow/react";

export default function InputNode({ data }) {
  return (
    <div className="p-2 border rounded bg-white shadow">
      <div>{data.label}</div>
      <Handle type="source" position="right" />
    </div>
  );
}
