import { useState } from 'react'
import PdfUploadModal from '../PdfUploadModal'

function ModalTestPage() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleUpload = (file: File) => {
    setUploadedFile(file)
    console.log('File uploaded:', file.name)
  }

  return (
    <div style={{ padding: 'var(--spacing-3xl)', textAlign: 'center' }}>
      <h1>Modal Test Page</h1>
      <p style={{ marginBottom: 'var(--spacing-2xl)', color: 'var(--text-gray)' }}>
        Test the PDF upload modal component
      </p>

      <button
        onClick={() => setIsModalOpen(true)}
        style={{
          padding: 'var(--spacing-sm) var(--spacing-xl)',
          fontSize: 'var(--font-size-md)',
          fontWeight: 'var(--font-weight-medium)',
          color: 'var(--white)',
          backgroundColor: 'var(--primary-blue)',
          border: 'none',
          borderRadius: 'var(--radius-lg)',
          cursor: 'pointer',
          transition: 'background-color var(--transition-fast)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = 'var(--primary-blue-hover)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = 'var(--primary-blue)'
        }}
      >
        Open Upload Modal
      </button>

      {uploadedFile && (
        <div
          style={{
            marginTop: 'var(--spacing-2xl)',
            padding: 'var(--spacing-md)',
            backgroundColor: 'var(--success-bg)',
            border: '1px solid var(--success-border)',
            borderRadius: 'var(--radius-lg)',
            maxWidth: '500px',
            margin: 'var(--spacing-2xl) auto 0',
          }}
        >
          <h3 style={{ margin: '0 0 var(--spacing-xs) 0', color: 'var(--success-heading)' }}>
            File Selected in Modal
          </h3>
          <p style={{ margin: 0, color: 'var(--success-text)' }}>
            <strong>Name:</strong> {uploadedFile.name}
          </p>
          <p style={{ margin: 0, color: 'var(--success-text)' }}>
            <strong>Size:</strong> {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
          </p>
          <p style={{ margin: 0, color: 'var(--success-text)' }}>
            <strong>Type:</strong> {uploadedFile.type}
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

export default ModalTestPage
