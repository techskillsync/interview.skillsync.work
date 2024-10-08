import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { MicAccessProvider } from "./components/MicAccessContext"
import { QuestionsProvider } from './components/QuestionsContext'
import Root from './routes/root/Root'
import SetupInterview from './routes/setup-interview/SetupInterview'
import PreInterview from './routes/preinterview/PreInterview'
import Interviewing from './routes/interviewing/Interviewing'
import Microphone from './components/Microphone'

function App() {
	return (
		<QuestionsProvider>
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
		</QuestionsProvider>
	)
}

export default App
