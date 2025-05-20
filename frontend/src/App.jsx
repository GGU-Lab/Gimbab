import { useCallback, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';

import InputNode from '@/components/nodes/InputNode';
import ModelNode from '@/components/nodes/ModelNode';
import OutputNode from '@/components/nodes/OutputNode';

import Sidebar from '@/components/panels/Sidebar';
import Topbar from '@/components/panels/Topbar';
import PropertyPanel from '@/components/panels/PropertyPanel';

const nodeTypes = {
  inputNode: InputNode,
  modelNode: ModelNode,
  outputNode: OutputNode,
};

let nodeId = 0;

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selected, setSelected] = useState(null);

  const onConnect = (params) => {
    if (!params.source || !params.target) return;
    setEdges((eds) => addEdge({ ...params, type: 'smoothstep' }, eds));
  };

  const onInit = useCallback((reactFlowInstance) => {
    reactFlowInstance.fitView();
  }, []);

  // 드래그 오버 시 기본 동작 방지
  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // 캔버스에 드롭 시 노드 추가
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const type = event.dataTransfer.getData('application/reactflow');
      if (!type) return;

      const bounds = event.currentTarget.getBoundingClientRect();
      const position = {
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      };

      const newNode = {
        id: `node-${nodeId++}`,
        type,
        position,
        data: { label: `New ${type}` },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [setNodes]
  );

  return (
    <div className="w-screen h-screen flex flex-col">
      <Topbar onRun={() => alert('실행')} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
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
            onNodeClick={(_, node) => setSelected(node)}
          >
            <Background color="#e5e7eb" />
            <MiniMap />
            <Controls position="bottom-left" />
          </ReactFlow>
        </div>
        <PropertyPanel selectedNode={selected} />
      </div>
    </div>
  );
}
