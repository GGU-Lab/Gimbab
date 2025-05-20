import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState
} from "@xyflow/react"; 
import "@xyflow/react/dist/style.css";
import InputNode from "@/components/nodes/InputNode";
import ModelNode from "@/components/nodes/ModelNode";
import OutputNode from "@/components/nodes/OutputNode";

const nodeTypes = {
  inputNode: InputNode,
  modelNode: ModelNode,
  outputNode: OutputNode,
};

const initialNodes = [
  {
    id: "input",
    type: "inputNode",
    data: { label: "Text Input" },
    position: { x: 100, y: 100 },
  },
  {
    id: "model",
    type: "modelNode",
    data: { label: "KcBERT" },
    position: { x: 300, y: 100 },
  },
  {
    id: "output",
    type: "outputNode",
    data: { label: "JSON Output" },
    position: { x: 500, y: 100 },
  },
];

const initialEdges = [
  { id: "e1-2", source: "input", target: "model" },
  { id: "e2-3", source: "model", target: "output" },
];

export default function PipelineBuilder() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background />
        <MiniMap />
        <Controls />
      </ReactFlow>
    </div>
  );
}
