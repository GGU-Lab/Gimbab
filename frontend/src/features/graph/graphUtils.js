export function convertNodeType(type) {
  if (type === "inputNode") return "input";
  if (type === "outputNode") return "output";
  if (type === "modelNode") return "model";
  return "bridge";
}

export function guessModuleFromType(type) {
  if (type === "inputNode") return "plain_text";
  if (type === "outputNode") return "json_output";
  if (type === "modelNode") return "hf_pipeline_runner";
  return "bridge_module";
}

export function buildGraphPayload(nodes, edges) {
  return {
    nodes: nodes.map((node) => ({
      id: node.id,
      type: convertNodeType(node.type),
      module: node.data.module || guessModuleFromType(node.type),
      params: node.data.params || {},
      evaluators: node.data.evaluators || [],
    })),
    edges: edges.map((e) => ({ from: e.source, to: e.target })),
  };
}

export function logPayload(graphPayload) {
  console.log("🟩 [Payload] nodes:");
  graphPayload.nodes.forEach((node) => {
    console.log(`- ${node.id}: type=${node.type}, module=${node.module}`);
    if (Object.keys(node.params).length > 0) console.log("  params:", node.params);
    if (node.evaluators.length > 0) console.log("  evaluators:", node.evaluators);
  });
  console.log("🔷 [Payload] edges:");
  graphPayload.edges.forEach((edge) => {
    console.log(`- ${edge.from} → ${edge.to}`);
  });
}
