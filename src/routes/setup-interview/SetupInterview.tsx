import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

function SetupInterview() {

	const navigate = useNavigate()
	const location = useLocation()
	const [questions, setQuestions] = useState<string[]|null>(null)

	async function getQuestions(): Promise<string[]> {
		return [
			"Introduce yourself",
			"Tell me about the microservice you deployed at SkillSync. From what I understand microservices are meant to handle one specific task, hiding the complexity with a simple REST API. Is that correct? If so how did you ensure your microservice was simple to use while performing complicated tasks under the hood?",
			"At UBC Agrobot what did you do when your vision for the website differed from a teammate?",
			"I see on your resume you made a Chess Engine, tell me about an improvement you made to it. What did you change that was not working like you wanted. How did you make it work how you wanted?",
		]
	}

	useEffect(() => {
		if (!questions) { return }
		navigate({ pathname: "/pre-interview", search: location.search })
	}, [questions])

	useEffect(() => {
		async function doAsync() {
			setQuestions(await getQuestions())
		}
		doAsync()
	}, [])


	return (
		<div className="flex flex-col justify-center items-center">
			<h1>We are grabbing your interviewer, sit tight while she arrives.</h1>
			<img src="/images/loading.gif" width={64}/>
		</div>
	)
}

export default SetupInterview