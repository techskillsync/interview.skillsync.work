import { createContext, useContext, useState, useEffect } from "react";

type UnprocessedQuestions = {
	"text": string,
	"audioB64": string
}

type Questions = {
	"text": string,
	"audioURL": string,
}

type QuestionsContext = {
	questions: Questions[] | undefined
}

const QuestionsContext = createContext<QuestionsContext>({questions: undefined})

function useQuestions(): QuestionsContext {
	const context = useContext(QuestionsContext)
	if (context === undefined) {
		throw new Error("useQuestions must be used within a QuestionsProvider")
	}
	return context
}

interface QuestionProviderProps { children: React.ReactNode }
function QuestionsProvider({ children }: QuestionProviderProps) {
	const [questions, setQuestions] = useState<QuestionsContext>({questions: undefined})

	useEffect(() => {
		fetch("http://localhost:8000/api/dummy-get-questions?uuid=123")
			.then(response => response.json())
			.then((data: UnprocessedQuestions[]) => {
				let processed_questions = []

				for (const q of data) {
					const binaryString = window.atob(q.audioB64)
					const binaryArray = new Uint8Array(binaryString.length)
					for (let i = 0; i < binaryString.length; i++) {
						binaryArray[i] = binaryString.charCodeAt(i)
					}
					const audioBlob = new Blob([binaryArray], { type: 'audio/mp3' })
					const audioURL = URL.createObjectURL(audioBlob)

					processed_questions.push({"text": q.text, "audioURL": audioURL})
				}

				setQuestions({questions: processed_questions})
			})
			.catch(error => {
				console.error("Error fetching questions:", error);
			});
	}, [])

	return (
		<QuestionsContext.Provider value={questions}>
			{children}
		</QuestionsContext.Provider>
	);
}

export type { Questions } 
export { useQuestions, QuestionsProvider }
export default QuestionsContext