import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Root from './routes/root/Root'
import Interviewing from './routes/interviewing/Interviewing';

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Root/>} />
				<Route path="/interviewing" element={<Interviewing/>} />
			</Routes>
		</Router>
	)
}

export default App
