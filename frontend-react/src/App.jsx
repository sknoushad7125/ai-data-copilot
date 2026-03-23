import { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [file, setFile] = useState(null);

  // Upload file
  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${BASE_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    alert("File uploaded!");
    console.log(data);
  };

  // Ask query
  const askQuery = async () => {
    const res = await fetch(`${BASE_URL}/ask?query=${query}`);
    const data = await res.json();
    setResponse(data);
  };

  return (
    <div className="app">

      <h1>AI Data Copilot Dashboard</h1>

      {/* Upload Section */}
      <div className="card">
        <h2>Upload File</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile}>Upload</button>
      </div>

      {/* Ask Section */}
      <div className="card">
        <h2>Ask Query</h2>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. top customers, summarize report"
        />
        <button onClick={askQuery}>Ask</button>
      </div>

      {/* Result Section */}
      {response && (
        <div className="card">
          <h2>Result</h2>

          <p><b>Type:</b> {response.type}</p>

          {response.generated_sql && (
            <>
              <p><b>Generated SQL:</b></p>
              <pre>{response.generated_sql}</pre>
            </>
          )}

          {response.answer && (
            <>
              <p><b>Answer:</b></p>
              <pre>{response.answer}</pre>
            </>
          )}

          {response.result && (
            <>
              <p><b>Data:</b></p>
              <pre>{JSON.stringify(response.result, null, 2)}</pre>
            </>
          )}

          {response.explanation && (
            <>
              <p><b>Explanation:</b></p>
              <pre>{JSON.stringify(response.explanation, null, 2)}</pre>
            </>
          )}
        </div>
      )}

    </div>
  );
}

export default App;