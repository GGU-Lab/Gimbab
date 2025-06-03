import { runPipeline } from '@/services/pipelineAPI';
import { buildGraphPayload, logPayload } from '../graph/graphUtils';

export function useRunPipeline({ nodes, edges, setLogs, setResult, setSelected }) {
  const handleRun = async () => {
    setSelected(null);
    const graphPayload = buildGraphPayload(nodes, edges);
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

  return { handleRun };
}
