import React, { useState } from 'react';
import axios from 'axios';
import { JSONTree } from 'react-json-tree';
import Switch from 'react-switch';
import './App.css';

const App = () => {
  const [pipeline, setPipeline] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState(false);

  const handlePipelineChange = (event) => {
    setPipeline(event.target.value);
  };

  const executePipeline = async () => {
    try {
      console.log("Sending request to /docs/");
      const response = await axios.post('http://localhost:8000/docs/', {
        pipeline: JSON.parse(pipeline)
      });
      console.log("Response received:", response.data);
      setResult(response.data.result);
      setError(null);
    } catch (err) {
      console.error('Error executing pipeline:', err);
      setError('Error executing pipeline');
      setResult(null);
    }
  };

  const handleViewModeChange = (checked) => {
    setViewMode(checked);
  };

  return (
    <div className="container">
      <h1 className="title">MongoDB Aggregation Pipeline UI</h1>
      <textarea
        className="pipeline-input"
        rows="10"
        cols="50"
        value={pipeline}
        onChange={handlePipelineChange}
        placeholder='Enter MongoDB aggregation pipeline as JSON (e.g., [{"$match": {"state": "BR"}}])'
      />
      <br />
      <div className="controls">
        <label className="switch-label">
          <span>Simple Format</span>
          <div className="switch-margin">
            <Switch
              onChange={handleViewModeChange}
              checked={viewMode}
              offColor="#888"
              onColor="#0D6EFD"
              uncheckedIcon={false}
              checkedIcon={false}
            />
          </div>
          <span>JSON View</span>
        </label>
        <button className="execute-button" onClick={executePipeline}>Execute Pipeline</button>
      </div>
      <br />
      {error && <p className="error-message">{error}</p>}
      {result && (
        <div className="result-output">
          {viewMode ? (
            <JSONTree data={result} />
          ) : (
            <pre>{JSON.stringify(result, null, 2)}</pre>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
