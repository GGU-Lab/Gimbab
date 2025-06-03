import { useCallback } from 'react';
import { addEdge } from '@xyflow/react';

let nodeId = 0;

export function useGraphHandlers({ setNodes, setEdges }) {
  const onConnect = useCallback((params) => {
    setEdges((eds) => {
      const isDuplicate = eds.some((e) => e.source === params.source && e.target === params.target);
      if (isDuplicate) return eds;
      return addEdge({ ...params, type: 'step' }, eds);
    });
  }, [setEdges]);

  const onInit = useCallback((instance) => {
    setTimeout(() => instance.fitView(), 0);
  }, []);

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback((event) => {
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
  }, [setNodes]);

  return { onDrop, onDragOver, onConnect, onInit };
}
