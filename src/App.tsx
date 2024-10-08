import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { MicAccessProvider } from "./components/microphone/MicAccessContext"
import Root from './routes/root/Root'
import SetupInterview from './routes/setup-interview/SetupInterview'
import PreInterview from './routes/preinterview/PreInterview'
import Interviewing from './routes/interviewing/Interviewing'
import Microphone from './components/microphone/Microphone'

function App() {
	return (
		<MicAccessProvider>
			<Router>
				<Routes>
					<Route path="/" element={<Root />} />
					<Route path="/setup-interview" element={<SetupInterview />} />
					<Route path="/preinterview" element={<PreInterview />} />
					<Route path="/interviewing" element={<Interviewing />} />
				</Routes>
				<Microphone />
			</Router>
		</MicAccessProvider>
	)
}

export default App
