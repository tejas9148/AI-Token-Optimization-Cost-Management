import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard/Dashboard';
import Ask from './pages/Ask/Ask';
import Chat from './pages/Chat/Chat';
import History from './pages/History/History';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background text-foreground">
        {/* Navigation */}
        <nav className="bg-primary text-primary-foreground px-4 py-3 shadow-sm">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-xl font-semibold">
                TokenWise
              </Link>
            </div>
            <div className="hidden md:flex space-x-4">
              <NavLink to="/" end className="{({ isActive }) =>
                `px-3 py-2 rounded-md text-sm font-medium ${isActive ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/20'}`}"
              >
                Dashboard
              </NavLink>
              <NavLink to="/ask" end className="{({ isActive }) =>
                `px-3 py-2 rounded-md text-sm font-medium ${isActive ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/20'}`}"
              >
                Ask
              </NavLink>
              <NavLink to="/chat" end className="{({ isActive }) =>
                `px-3 py-2 rounded-md text-sm font-medium ${isActive ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/20'}`}"
              >
                Chat
              </NavLink>
              <NavLink to="/history" end className="{({ isActive }) =>
                `px-3 py-2 rounded-md text-sm font-medium ${isActive ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/20'}`}"
              >
                History
              </NavLink>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="pt-6 pb-10 max-w-7xl mx-auto px-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/ask" element={<Ask />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/history" element={<History />} />
            <Route path="*" element={<div className="p-6">
              <h1 className="text-2xl font-bold">404 - Page Not Found</h1>
              <p className="text-muted-foreground">The page you're looking for doesn't exist.</p>
              <Link to="/" className="mt-4 inline-block text-primary hover:text-primary/80">
                Go Home
              </Link>
            </div>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;