export default function PropertyPanel({ selectedNode }) {
  return (
    <div className="w-64 p-4 border-l bg-white">
      <h3 className="text-lg font-semibold mb-4">속성</h3>
      {selectedNode ? (
        <div className="space-y-2 text-sm">
          <div><span className="font-medium">ID:</span> {selectedNode.id}</div>
          <div><span className="font-medium">Type:</span> {selectedNode.type}</div>
          <div><span className="font-medium">Label:</span> {selectedNode.data?.label}</div>
        </div>
      ) : (
        <div className="text-gray-500 text-sm">노드를 선택하세요.</div>
      )}
    </div>
  );
}
