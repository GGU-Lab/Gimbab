// src/services/pipelineAPI.js
import axios from 'axios';

export async function runPipeline(pipelineJson) {
  const response = await axios.post('http://localhost:8000/pipeline/graph/run', pipelineJson);
  return response.data;
}
