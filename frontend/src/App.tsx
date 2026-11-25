import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState<string>("Loading...");

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/v1/health`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "ok") {
          setStatus("Backend: ok");
        } else {
          setStatus(`Backend error: ${JSON.stringify(data)}`);
        }
      })
      .catch((err) => {
        setStatus(`Backend unreachable: ${err.message}`);
      });
  }, []);

  return (
    <div className="flex items-center justify-center h-screen text-2xl">
      {status}
    </div>
  );
}

export default App;
