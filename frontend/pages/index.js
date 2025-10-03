import { useState } from 'react'

export default function Home() {
  const [file, setFile] = useState(null)
  const [pointersText, setPointersText] = useState(
    'List all dates\nWho signed?\nTotal contract value?'
  )
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return alert('Please choose a PDF')

    const pointers = pointersText.split('\n').map((s) => s.trim()).filter(Boolean)
    const form = new FormData()
    form.append('file', file)
    form.append('pointers', JSON.stringify(pointers))

    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: form
      })
      const data = await res.json()
      setResults(data)
    } catch (err) {
      console.error(err)
      alert('Error contacting backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>PDF Facts Analyzer</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>PDF file</label><br />
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>

        <div style={{ marginTop: 12 }}>
          <label>Pointers (one per line)</label><br />
          <textarea
            rows={6}
            cols={60}
            value={pointersText}
            onChange={(e) => setPointersText(e.target.value)}
          />
        </div>

        <div style={{ marginTop: 12 }}>
          <button type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </form>

      {results && (
        <section style={{ marginTop: 24 }}>
          <h2>Results</h2>
          {results.map((item) => (
            <div
              key={item.pointer}
              style={{ marginBottom: 16, border: '1px solid #eee', padding: 12 }}
            >
              <h3>{item.pointer}</h3>
              {item.results.length === 0 && <p><i>No matches found</i></p>}
              {item.results.map((r, idx) => (
                <div key={idx} style={{ marginBottom: 8 }}>
                  <strong>Page:</strong> {r.page} — <strong>chars:</strong> {r.start_char}-{r.end_char}
                  <div style={{ marginTop: 6, whiteSpace: 'pre-wrap', background: '#fafafa', padding: 8 }}>
                    {r.snippet}
                  </div>
                  <div style={{ fontSize: 12, color: '#666' }}>{r.rationale}</div>
                </div>
              ))}
            </div>
          ))}
        </section>
      )}
    </main>
  )
}
