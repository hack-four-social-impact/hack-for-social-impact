import { useState } from 'react'
import './App.css'
import PdfUploadModal from './PdfUploadModal'

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleUpload = (file: File) => {
    setUploadedFile(file)
    console.log('File uploaded:', file.name)
    // TODO: Send file to backend API
  }

  return (
    <div style={{ padding: '40px', textAlign: 'center' }}>
      <h1>Hack for Social Impact</h1>
      <p style={{ marginBottom: '32px', color: '#6b7280' }}>
        PDF Processing Application
      </p>

      <button
        onClick={() => setIsModalOpen(true)}
        style={{
          padding: '12px 24px',
          fontSize: '16px',
          fontWeight: '500',
          color: '#ffffff',
          backgroundColor: '#2563eb',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          transition: 'background-color 0.2s',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = '#1d4ed8'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = '#2563eb'
        }}
      >
        Upload PDF
      </button>

      {uploadedFile && (
        <div
          style={{
            marginTop: '32px',
            padding: '16px',
            backgroundColor: '#f0fdf4',
            border: '1px solid #86efac',
            borderRadius: '8px',
            maxWidth: '500px',
            margin: '32px auto 0',
          }}
        >
          <h3 style={{ margin: '0 0 8px 0', color: '#166534' }}>
            File Uploaded Successfully
          </h3>
          <p style={{ margin: 0, color: '#15803d' }}>
            {uploadedFile.name} ({(uploadedFile.size / 1024 / 1024).toFixed(2)} MB)
          </p>
        </div>
      )}

      <PdfUploadModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onUpload={handleUpload}
      />
    </div>
  )
}

export default App
