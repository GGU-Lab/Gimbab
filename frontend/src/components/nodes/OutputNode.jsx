import React from "react";
import { Handle } from "@xyflow/react";

export default function OutputNode({ data }) {
  return (
    <div className="p-2 border rounded bg-white shadow">
      <Handle type="target" position="left" />
      <div>{data.label}</div>
    </div>
  );
}
