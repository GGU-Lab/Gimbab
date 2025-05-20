// src/hooks/usePipelineToJson.js
export function usePipelineToJson(nodes, edges) {
  return () => {
    const inputNode = nodes.find((n) => n.type === 'inputNode');
    const outputNode = nodes.find((n) => n.type === 'outputNode');

    const modelNodes = nodes
      .filter((n) => n.type === 'modelNode')
      .sort((a, b) => a.position.x - b.position.x); // 좌우 순 정렬

    return {
      input_data: '오늘 너무 졸리다.', // 임시 입력
      input_adapter: inputNode?.data.moduleName || inputNode?.id,
      models: modelNodes.map((n) => n.data.moduleName || n.id),
      output_adapter: outputNode?.data.moduleName || outputNode?.id,
    };
  };
}
