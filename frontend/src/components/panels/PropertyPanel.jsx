export default function PropertyPanel({ selectedNode, result, logs }) {
  return (
    <div className="w-64 p-4 border-l bg-white overflow-y-auto text-sm">
      <h3 className="text-lg font-semibold mb-4">속성 / 결과</h3>

      {selectedNode ? (
        <div className="space-y-2">
          <div><span className="font-medium">🆔 ID:</span> {selectedNode.id}</div>
          <div><span className="font-medium">🔧 Type:</span> {selectedNode.type}</div>
          <div><span className="font-medium">🏷 Label:</span> {selectedNode.data?.label}</div>
        </div>
      ) : result ? (
        <>
          <div className="mb-2">
            <div className="font-medium text-gray-600">✅ 실행 결과</div>
            <pre className="p-2 bg-gray-100 border rounded text-xs overflow-x-auto whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>

          <div className="mt-4">
            <div className="font-medium text-gray-600">📊 실행 로그</div>
            <table className="w-full mt-2 text-xs">
              <thead>
                <tr className="text-left border-b">
                  <th>Step</th>
                  <th>Time (s)</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log, idx) => (
                  <tr key={idx} className="border-b">
                    <td className="py-1">{log.step}</td>
                    <td className="py-1">{log.elapsed}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <div className="text-gray-500">노드를 선택하거나 실행해 주세요.</div>
      )}
    </div>
  );
}
