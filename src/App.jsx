import { useEffect, useState } from "react";

function App() {
  const [digests, setDigests] = useState([]);

  useEffect(() => {
    fetch("/stock-digest-site/digests/index.json")
      .then(res => res.json())
      .then(data => setDigests(data));
  }, []);

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">📊 국내 주식시장 요약 모음</h1>
      <ul className="space-y-4">
        {digests.map(d => (
          <li key={d.date}>
            <a
              className="text-blue-600 hover:underline"
              href={`/stock-digest-site/digests/${d.file}`}
              target="_blank"
              rel="noreferrer"
            >
              {d.date} 요약 보기
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
