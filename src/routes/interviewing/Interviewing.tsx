import { useState, useEffect } from 'react'
import { useQuestions } from "../../components/QuestionsContext";

function Interviewing() {

	const QuestionsContext = useQuestions()
	const [questionIndex, setQuestionIndex] = useState<number>(0)
	const [currentQuestionText, setCurrentQuestionText] = useState<string|undefined>(undefined)


	async function play_next_question(): Promise<boolean> {
		const audio_element = document.getElementById('audio-player')
		if (!(audio_element instanceof HTMLAudioElement)) {
			console.warn ("Could not find audio element to give audio to!")
			return false
		}

		if (!audio_element.paused && !audio_element.ended) {
			console.warn("Refusing to play next question. Audio is still playing")
			return false
		}

		if (!QuestionsContext.questions) { return false }
		if (questionIndex >= QuestionsContext.questions.length) { return false }

		// ========== TEMPORARY DELAY FOR DEMO PURPOSE ==========
		if (questionIndex !== 0) { await new Promise(r => setTimeout(r, 4000)); } 
		// ========== TEMPORARY DELAY FOR DEMO PURPOSE ==========

		const result = ask_question()
		return result
	}

	function ask_question(): boolean {
		if (!QuestionsContext.questions) { return false }

		console.log("Question index: " + questionIndex)
		const question = QuestionsContext.questions[questionIndex]
		setCurrentQuestionText(question.text)
		const audio_element = document.getElementById('audio-player')
		if (!(audio_element instanceof HTMLAudioElement)) {
			console.warn ("Could not find audio element to give audio to!")
			return false
		}

		audio_element.src = question.audioURL
		audio_element.load()
		// React's double loads will cause this to error every time.
		// I catch the error and do nothing so the console isn't spammed
		audio_element.play().catch(error => error)
		
		setQuestionIndex(questionIndex + 1)

		return true
	}

	useEffect(() => {
		play_next_question()
		const audio_element = document.getElementById('audio-player')
		if (!(audio_element instanceof HTMLAudioElement)) {
			console.warn ("Could not find audio element to give audio to!")
			return
		}
		audio_element.addEventListener('pause', () => {audio_element.play})
		audio_element.addEventListener('ended', play_next_question)

		return () => {
			audio_element.removeEventListener('ended', play_next_question)
		}
	})

	return (
		<div className="w-[50%]">
			<h2>{currentQuestionText}</h2>
			<audio id="audio-player" controls={false} />
		</div>
	)
}

export default Interviewing;
