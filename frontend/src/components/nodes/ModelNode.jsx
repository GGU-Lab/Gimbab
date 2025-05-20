import React from "react";
import { Handle } from "@xyflow/react";

export default function ModelNode({ data }) {
  return (
    <div className="p-2 border rounded bg-white shadow">
      <Handle type="target" position="left" />
      <div>{data.label}</div>
      <Handle type="source" position="right" />
    </div>
  );
}
