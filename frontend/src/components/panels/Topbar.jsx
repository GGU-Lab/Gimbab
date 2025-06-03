import React from 'react';

export default function Topbar({ inputValue, onInputChange, onRun, onFileChange }) {
  return (
    <div className="flex items-center justify-between px-4 py-2 border-b bg-white shadow-sm">
      {/* 왼쪽 로고 */}
      <div className="flex items-center gap-2">
        <div className="text-xl font-bold text-blue-600">Gimbab</div>
      </div>

      {/* 중앙 입력창 */}
      <div className="flex-1 flex justify-center px-4">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => onInputChange(e.target.value)}
          placeholder="텍스트 입력..."
          className="w-full max-w-lg border border-gray-300 px-4 py-1 rounded text-sm shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      {/* 오른쪽 버튼 영역 */}
      <div className="flex items-center gap-2">
        <label className="cursor-pointer text-xs px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 text-gray-800 shadow-sm">
          📎 파일 선택
          <input type="file" hidden onChange={onFileChange} />
        </label>
        <button
          onClick={onRun}
          className="px-4 py-1 rounded bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 text-white text-sm font-semibold shadow-md"
        >
          실행
        </button>
      </div>
    </div>
  );
}
