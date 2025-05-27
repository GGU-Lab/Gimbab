export default function Topbar({ onRun }) {
  return (
    <div className="h-12 flex items-center justify-between px-4 border-b bg-gray-100">
      <input
        type="text"
        placeholder="입력 텍스트"
        className="flex-1 mr-4 px-2 py-1 border rounded"
      />
      <button
        onClick={onRun}
        className="px-4 py-1 bg-blue-600 text-black rounded hover:bg-blue-700"
      >
        실행 ▶
      </button>
    </div>
  );
}
