import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { MicAccessProvider } from "./components/MicAccessContext"
import { QuestionsProvider } from './components/QuestionsContext'
import CheckRequirements from './components/CheckRequirements'
import Root from './routes/root/Root'
import SetupInterview from './routes/setup-interview/SetupInterview'
import PreInterview from './routes/pre-interview/PreInterview'
import Interviewing from './routes/interviewing/Interviewing'
import Error from './routes/error/Error'
import Microphone from './components/Microphone'

function App() {
	return (
		<QuestionsProvider>
			<MicAccessProvider>
				<Router>
					<CheckRequirements />
					<Routes>
						<Route path="/" element={<Root />} />
						<Route path="/setup-interview" element={<SetupInterview />} />
						<Route path="/pre-interview" element={<PreInterview />} />
						<Route path="/interviewing" element={<Interviewing />} />
						<Route path="/error/*" element={<Error />} />
					</Routes>
					<Microphone />
				</Router>
			</MicAccessProvider>
		</QuestionsProvider>
	)
}

export default App
