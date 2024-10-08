import { useState, useEffect } from 'react'
import { useQuestions } from "../../components/QuestionsContext";

type ProcessedQuestions = {
	"text": string,
	"audioURL": string
}

function Interviewing() {

	const QuestionsContext = useQuestions()

	useEffect(() => {
		if (!QuestionsContext.questions) { return }

		for (const q of QuestionsContext.questions) {

			const audioElement = document.getElementById('audio-player')
			if (!audioElement || !(audioElement instanceof HTMLAudioElement)) {
				console.warn("Could not find audio element to give audio to!")
				return
			}
			audioElement.src = q.audioURL
			audioElement.controls = false
			audioElement.load()
			// React's double loads will cause this to error every time.
			// I catch the error and do nothing so the console isn't spammed
			audioElement.play().catch((error) => error)
		}
	}, [])
	return (
		<div className="w-[50%] bg-sky-200">
			<h2>...</h2>
			<audio id="audio-player" />
		</div>
	)
}

export default Interviewing;
