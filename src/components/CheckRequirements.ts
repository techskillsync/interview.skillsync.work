import { useEffect } from 'react'
import { NavigateFunction, useLocation, useNavigate } from "react-router-dom"
import { useMicAccess } from "./MicAccessContext"
import QuestionsContext from './QuestionsContext'
import { useQuestions } from "./QuestionsContext"

const uuid_checked_routes: Array<string> = ["/", "/setup-interview", "/pre-interview", "/interviewing"]
const mic_checked_routes: Array<string> = ["/setup-interview", "/pre-interview", "/interviewing"]
const questions_checked_routes: Array<string> = ["/pre-interview", "/interviewing"]

/*
 * Using the current url, runs a series of checks. If any of them fail the user
 * is redirected to /error/[error-msg]?error_msg=<Error&Message>
 */
function CheckRequirements() {

	const location = useLocation()
	const navigate = useNavigate()
	const { pathname, search } = location
	const params = new URLSearchParams(search)
	const { has_mic_access } = useMicAccess()
	const questions_context = useQuestions()

	useEffect(() => {
		uuid_check(pathname, params, navigate)
		questions_check(pathname, questions_context, navigate)
	}, [])

	useEffect(() => {
		mic_check(pathname, has_mic_access, navigate)
	}, [has_mic_access])

	return null
}

/*
 * Ensures there is a uuid param, if not routes the user to /no-uuid
 */
function uuid_check(pathname: string, params: URLSearchParams, navigate: NavigateFunction): boolean {

	if (!uuid_checked_routes.includes(pathname)) { return true }

	const entries = Array.from(params.keys())

	if (!entries.includes('uuid')) {
		navigate({ pathname: "/error/no-uuid", search: location.search + "&error_msg=Could not find uuid in url params" })
		return false
	}

	return true
}

function mic_check(pathname: string, has_mic_access: boolean, navigate: NavigateFunction) {
	if (!mic_checked_routes.includes(pathname)) { return true }
	if (!has_mic_access) {
		navigate({ pathname: "/error/no-mic", search: location.search + "&error_msg=Could not access microphone" })
		return false
	}
	return true
}

function questions_check(pathname: string, questions_context: QuestionsContext, navigate: NavigateFunction) {
	if (!questions_checked_routes.includes(pathname)) { return true }
	if (!questions_context.questions) {
		console.log("questions: " + questions_context.questions)
		navigate({pathname: "/error/no-questions", search: location.search + "&error_msg=Did not receive questions from the backend"})
		return false
	}
	return true
}
	
export default CheckRequirements