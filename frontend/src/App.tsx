import { useState } from 'react'
import './App.css'
import ModalTestPage from './pages/ModalTestPage'
import ApiTestPage from './pages/ApiTestPage'

type Page = 'modal' | 'api'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('modal')

  const navButtonStyle = (page: Page) => ({
    padding: '10px 20px',
    fontSize: 'var(--font-size-sm)',
    fontWeight: 'var(--font-weight-medium)',
    color: currentPage === page ? 'var(--white)' : 'var(--text-gray-dark)',
    backgroundColor: currentPage === page ? 'var(--primary-blue)' : 'var(--neutral-border)',
    border: currentPage === page ? 'none' : '2px solid var(--black)',
    borderRadius: 'var(--radius-md)',
    cursor: 'pointer',
    transition: 'all var(--transition-fast)',
  })

  return (
    <div>
      {/* Navigation Bar */}
      <nav
        style={{
          backgroundColor: 'var(--white)',
          borderBottom: '1px solid var(--neutral-border)',
          padding: 'var(--spacing-md) var(--spacing-xl)',
          display: 'flex',
          gap: 'var(--spacing-sm)',
          alignItems: 'center',
        }}
      >
        <h2 style={{ margin: 0, marginRight: 'var(--spacing-xl)', fontSize: '18px' }}>
          Test Pages
        </h2>
        <button
          onClick={() => setCurrentPage('modal')}
          style={navButtonStyle('modal')}
          onMouseEnter={(e) => {
            if (currentPage !== 'modal') {
              e.currentTarget.style.backgroundColor = 'var(--nav-inactive)'
            }
          }}
          onMouseLeave={(e) => {
            if (currentPage !== 'modal') {
              e.currentTarget.style.backgroundColor = 'var(--neutral-border)'
            }
          }}
        >
          Modal Test
        </button>
        <button
          onClick={() => setCurrentPage('api')}
          style={navButtonStyle('api')}
          onMouseEnter={(e) => {
            if (currentPage !== 'api') {
              e.currentTarget.style.backgroundColor = 'var(--nav-inactive)'
            }
          }}
          onMouseLeave={(e) => {
            if (currentPage !== 'api') {
              e.currentTarget.style.backgroundColor = 'var(--neutral-border)'
            }
          }}
        >
          API Test
        </button>
      </nav>

      {/* Page Content */}
      <div>
        {currentPage === 'modal' && <ModalTestPage />}
        {currentPage === 'api' && <ApiTestPage />}
      </div>
    </div>
  )
}

export default App
