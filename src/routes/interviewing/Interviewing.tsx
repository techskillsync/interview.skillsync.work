import { useState, useEffect } from "react"
function Interviewing() {

	const [questionText, setQuestionText] = useState<string>("...");
	const prompt = "Tell me about a conceptual problem you solved in a recent project. How did you solve it? What approaches did you take?"

	async function askQuestion(question:string) {
		try {
			const response = await fetch("http://localhost:8000/api/get-audio-dummy", {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({"question":question})
			});

			if (!response.ok) {
				console.log(response)
				throw Error(response.statusText)
			}

			const audioBlob = await response.blob();
			const audioUrl = URL.createObjectURL(audioBlob);

			const audioElement = document.getElementById('audio-player');
			if (!audioElement || !(audioElement instanceof HTMLAudioElement)) {
				console.warn("Could not find audio element to give audio to!")
				return
			}

			setQuestionText(question)
			audioElement.src = audioUrl
			audioElement.controls = false
			audioElement.load()
			// React's double loads will cause this to error every time.
			// I catch the error and do nothing so the console isn't spammed
			audioElement.play().catch((error) => error)

		} catch (error) {
			console.error('Error:', error)
		}
	}

	useEffect(() => {
		askQuestion(prompt);
	}, [])

	return (
		<div className="w-[50%] bg-sky-200">
			<h2>{questionText}</h2>
			<audio id="audio-player"/>
		</div>
	)
}

export default Interviewing;
