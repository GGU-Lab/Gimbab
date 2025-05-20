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
import { usePipelineToJson } from '@/hooks/usePipelineToJson';
import { runPipeline } from '@/services/pipelineAPI';

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
    const payload = toJson();
    console.log("payload: ", payload)
    try {
      // const res = await runPipeline(payload);
      // console.log('✅ 실행 결과:', res);
      // TODO: 실행 로그 state에 저장하여 우측 패널에서 표시
      // setResult(res.result);
      // setLogs(res.execution_logs);

      // 🧪 모의 실행 결과
      const mockResult = {
        label: '부정',
        confidence: 0.92,
      };

      const mockLogs = [
        { step: 'text_input', elapsed: 0.01 },
        { step: 'kcbert_sentiment', elapsed: 0.78 },
        { step: 'json_output', elapsed: 0.03 },
      ];

      setResult(mockResult);
      setLogs(mockLogs);
    } catch (err) {
      console.error('🚨 실행 실패:', err);
    }
  };

  const onConnect = (params) => {
    setEdges((eds) => addEdge({ ...params, type: 'step' }, eds));
    console.log("connect: ", edges)
  };

  const onInit = useCallback((instance) => {
    setTimeout(() => {
      instance.fitView();
    }, 0);
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
      <Topbar onRun={handleRun} />
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
            onNodeClick={(_, node) => { setSelected(node); setResult(null); setLogs([]); }}
          >
            <Background color="#e5e7eb" />
            <MiniMap />
            <Controls position="bottom-left" />
          </ReactFlow>
        </div>
        <PropertyPanel selectedNode={selected} result={result} logs={logs} />


      </div>
    </div>
  );
}
