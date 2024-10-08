import { createContext, useContext, useState, useEffect } from "react";

interface QuestionsContextType {
	questions: string[] | null;
}

const QuestionsContext = createContext<QuestionsContextType | undefined>(undefined)

function useQuestions(): QuestionsContextType {
	const context = useContext(QuestionsContext)
	if (context === undefined) {
		throw new Error("useQuestions must be used within a QuestionsProvider")
	}
	return context
}

interface QuestionProviderProps { children: React.ReactNode }
function QuestionsProvider({ children }: QuestionProviderProps) {
	const [questions, setQuestions] = useState<string[] | null>(null)

	useEffect(() => {
		const questions = [
			"Introduce yourself",
			"Tell me about the microservice you deployed at SkillSync. From what I understand microservices are meant to handle one specific task, hiding the complexity with a simple REST API. Is that correct? If so how did you ensure your microservice was simple to use while performing complicated tasks under the hood?",
			"At UBC Agrobot what did you do when your vision for the website differed from a teammate?",
			"I see on your resume you made a Chess Engine, tell me about an improvement you made to it. What did you change that was not working like you wanted. How did you make it work how you wanted?",
		]
		setQuestions(questions)
	}, [])

	return (
		<QuestionsContext.Provider value={{ questions }}>
			{children}
		</QuestionsContext.Provider>
	);
}

export { useQuestions, QuestionsProvider }
export default QuestionsContext