import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import SearchComponent from './components/search_component.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <SearchComponent />
      </div>
      
    </>
  )
}

export default App
