import { useState } from 'react'
import type { PdfProcessResponse } from '../services/api'
import { uploadPdfForProcessing } from '../services/api'

function ApiTestPage() {
  const [response, setResponse] = useState<PdfProcessResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleTestUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      console.log('Uploading file:', file.name)
      const result = await uploadPdfForProcessing(file)
      console.log('API Response:', result)
      setResponse(result)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error'
      console.error('API Error:', errorMessage)
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 'var(--spacing-lg)', maxWidth: '800px', margin: '0 auto' }}>
      <h2>API Service Layer Test</h2>

      <div style={{ marginBottom: 'var(--spacing-lg)' }}>
        <label
          htmlFor="test-file"
          style={{
            display: 'block',
            marginBottom: 'var(--spacing-xs)',
            fontWeight: 'var(--font-weight-medium)',
          }}
        >
          Select PDF to test API:
        </label>
        <input
          id="test-file"
          type="file"
          accept=".pdf"
          onChange={handleTestUpload}
          disabled={loading}
          style={{
            padding: 'var(--spacing-xs)',
            border: '1px solid var(--neutral-border-light)',
            borderRadius: 'var(--radius-sm)',
          }}
        />
      </div>

      {loading && (
        <div style={{ padding: 'var(--spacing-md)', backgroundColor: 'var(--info-bg)', borderRadius: 'var(--radius-sm)' }}>
          Loading... Processing PDF
        </div>
      )}

      {error && (
        <div style={{ padding: 'var(--spacing-md)', backgroundColor: 'var(--error-bg)', borderRadius: 'var(--radius-sm)', marginTop: 'var(--spacing-md)' }}>
          <h3 style={{ margin: '0 0 var(--spacing-xs) 0', color: 'var(--error-heading)' }}>Error</h3>
          <pre style={{ margin: 0, color: 'var(--error-text)', whiteSpace: 'pre-wrap' }}>{error}</pre>
        </div>
      )}

      {response && (
        <div style={{ marginTop: 'var(--spacing-md)' }}>
          <div style={{ padding: 'var(--spacing-md)', backgroundColor: 'var(--success-bg-alt)', borderRadius: 'var(--radius-sm)', marginBottom: 'var(--spacing-md)' }}>
            <h3 style={{ margin: '0 0 var(--spacing-xs) 0', color: 'var(--success-heading)' }}>Success!</h3>
            <p style={{ margin: 0, color: 'var(--success-text)' }}>File processed successfully</p>
          </div>

          <div style={{ padding: 'var(--spacing-md)', backgroundColor: 'var(--neutral-bg-medium)', borderRadius: 'var(--radius-sm)', marginBottom: 'var(--spacing-md)', border: '1px solid var(--neutral-border-dark)' }}>
            <h3 style={{ marginTop: 0 }}>Response Metadata:</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><strong>Filename:</strong> {response.filename}</li>
              <li><strong>File Size:</strong> {(response.file_size / 1024).toFixed(2)} KB</li>
              <li><strong>Text Length:</strong> {response.extracted_text_length} characters</li>
              <li><strong>Summary Type:</strong> {response.summary_type}</li>
            </ul>
          </div>

          <div style={{ padding: 'var(--spacing-md)', backgroundColor: 'var(--neutral-bg-medium)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--neutral-border-dark)' }}>
            <h3 style={{ marginTop: 0 }}>Markdown Summary:</h3>
            <pre style={{
              whiteSpace: 'pre-wrap',
              wordWrap: 'break-word',
              backgroundColor: 'var(--white)',
              padding: 'var(--spacing-sm)',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--neutral-border-dark)',
              maxHeight: '400px',
              overflow: 'auto',
            }}>
              {response.markdown_summary}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default ApiTestPage
