import { useCallback, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
  useReactFlow
} from '@xyflow/react';

import InputNode from '@/components/nodes/InputNode';
import ModelNode from '@/components/nodes/ModelNode';
import OutputNode from '@/components/nodes/OutputNode';

import Sidebar from '@/components/panels/Sidebar';
import Topbar from '@/components/panels/Topbar';
import PropertyPanel from '@/components/panels/PropertyPanel';
import { usePipelineToJson } from '@/hooks/usePipelineToJson';
import { runPipeline } from '@/services/pipelineAPI';
import './index.css';

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
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);

  const toJson = usePipelineToJson(nodes, edges);

  const handleRun = async () => {
    setSelected(null); // ✅ 실행 전에 속성 보기 해제

    const graphPayload = {
      nodes: nodes.map((node) => ({
        id: node.id,
        type: convertNodeType(node.type),
        module: node.data.module || guessModuleFromType(node.type),
        params: node.data.params || {},
        evaluators: node.data.evaluators || [],
      })),
      edges: edges.map((e) => ({ from: e.source, to: e.target })),
    };

    // payload 출력
    logPayload(graphPayload);

    try {
      const res = await runPipeline(graphPayload);
      console.log('✅ 실행 결과:', res);
      setResult(res.result);
      setLogs(res.execution_logs);
    } catch (err) {
      console.error('🚨 실행 실패:', err);
    }
  };

  function logPayload(graphPayload) {
    console.log("🟩 [Payload] nodes:");
    graphPayload.nodes.forEach((node) => {
      console.log(`- ${node.id}: type=${node.type}, module=${node.module}`);
      if (Object.keys(node.params).length > 0) {
        console.log("  params:", node.params);
      }
      if (node.evaluators.length > 0) {
        console.log("  evaluators:", node.evaluators);
      }
    });

    console.log("🔷 [Payload] edges:");
    graphPayload.edges.forEach((edge) => {
      console.log(`- ${edge.from} → ${edge.to}`);
    });

  }

  function convertNodeType(type) {
    if (type === "inputNode") return "input";
    if (type === "outputNode") return "output";
    if (type === "modelNode") return "model";
    return "bridge"; // or throw
  }

  function guessModuleFromType(type) {
    if (type === "inputNode") return "plain_text";
    if (type === "outputNode") return "json_output";
    if (type === "modelNode") return "hf_pipeline_runner";
    return "bridge_module"; // future
  }


  const onConnect = (params) => {
    setEdges((eds) => {
      const isDuplicate = eds.some(
        (e) => e.source === params.source && e.target === params.target
      );
      if (isDuplicate) return eds;
      return addEdge({ ...params, type: 'step' }, eds);
    });
  };


  const onInit = useCallback((instance) => {
    setTimeout(() => {
      instance.fitView(); // padding 넓히기
    }, 0);
  }, []);


  // 드래그 오버 시 기본 동작 방지
  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

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

      const nodeIdString = `node-${nodeId++}`;

      const newNode = {
        id: nodeIdString,
        type,
        position,
        data: {
          module: '',
          params: {},
          evaluators: [],
        },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [setNodes]
  );


  return (
    <div className="w-screen h-screen flex flex-col bg-gray-50">
      {/* Topbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b bg-white shadow-sm">
        {/* 왼쪽 로고 */}
        <div className="flex items-center gap-2">
          <div className="text-xl font-bold text-blue-600"> Gimbab</div>
        </div>

        {/* 중앙 입력창 */}
        <div className="flex-1 flex justify-center px-4">
          <input
            type="text"
            placeholder="텍스트 입력..."
            className="w-full max-w-lg border border-gray-300 px-4 py-1 rounded text-sm shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        {/* 오른쪽 버튼 영역 */}
        <div className="flex items-center gap-2">
          <label className="cursor-pointer text-xs px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 text-gray-800 shadow-sm">
            📎 파일 선택
            <input type="file" hidden />
          </label>
          <button
            onClick={handleRun}
            className="px-4 py-1 rounded bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 text-white text-sm font-semibold shadow-md"
          >
            실행
          </button>
        </div>
      </div>

      {/* Body */}
      <div className="flex flex-1">
        {/* 왼쪽 사이드바 */}
        <Sidebar nodes={nodes} edges={edges} />

        {/* 중앙 플로우 영역 */}
        <div
          className="flex-1 relative overflow-visible"
          onDrop={onDrop}
          onDragOver={onDragOver}
        >
          <div className="w-full h-full">
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
              className="w-full h-full"
            >
              <Background color="#e5e7eb" />
              <MiniMap />
              <Controls position="bottom-left" />
            </ReactFlow>
          </div>
        </div>

        {/* 오른쪽 속성 패널 */}
        <PropertyPanel
          selectedNode={selected}
          setNodes={setNodes}
          result={result}
        />
      </div>
    </div>


  );
}
