import { useNodesState, useEdgesState, ReactFlow, Background, Controls, MiniMap } from '@xyflow/react';
import { useState, useCallback } from 'react';

import InputNode from '@/components/nodes/InputNode';
import ModelNode from '@/components/nodes/ModelNode';
import OutputNode from '@/components/nodes/OutputNode';

import Sidebar from '@/components/panels/Sidebar';
import PropertyPanel from '@/components/panels/PropertyPanel';
import Topbar from '@/components/panels/Topbar';

import { useRunPipeline } from '@/features/execution/useRunPipeline';
import { useGraphHandlers } from '@/features/graph/useGraphHandlers';

import './index.css';

const nodeTypes = {
  inputNode: InputNode,
  modelNode: ModelNode,
  outputNode: OutputNode,
};

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selected, setSelected] = useState(null);
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);

  const {
    onDrop,
    onDragOver,
    onConnect,
    onInit
  } = useGraphHandlers({ setNodes, setEdges });

  const { handleRun } = useRunPipeline({
    nodes,
    edges,
    setLogs,
    setResult,
    setSelected
  });

  return (
    <div className="w-screen h-screen flex flex-col bg-gray-50">
      <Topbar onRun={handleRun} />
      <div className="flex flex-1">
        <Sidebar
          nodes={nodes}
          edges={edges}
          setNodes={setNodes}
          setEdges={setEdges}
        />
        <div className="flex-1 relative" onDrop={onDrop} onDragOver={onDragOver}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onInit={onInit}
            nodeTypes={nodeTypes}
            fitView
            onNodeClick={(_, node) => {
              setSelected(node);
              setResult(null);
              setLogs([]);
            }}
          >
            <Background color="#e5e7eb" />
            <MiniMap />
            <Controls position="bottom-left" />
          </ReactFlow>
        </div>
        <PropertyPanel selectedNode={selected} setNodes={setNodes} result={result} />
      </div>
    </div>
  );
}
