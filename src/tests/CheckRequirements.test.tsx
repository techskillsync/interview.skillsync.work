import { render, screen } from '@testing-library/react'
import App from '../App'
import '@testing-library/jest-dom'

test('Check Requirments - root page success', async () => {
	window.history.pushState({}, 'Test page', '/?uuid=123')
	render(<App />)
	expect(window.location.pathname).toEqual('/')
})

test('Check Requirements - uuid failure, should redirect and display useful error message', () => {
	const uuid_checked_routes: Array<string> = ["/", "/setup-interview", "/pre-interview", "/interviewing"]

	uuid_checked_routes.forEach(route => {
		window.history.pushState({}, 'Test page', route)
		render(<App />)
		expect(window.location.pathname.startsWith('/error/')).toBe(true)
		const elements = screen.getAllByText("Could not find uuid in url params")
		expect(elements.length).toBeGreaterThan(0)
		expect(elements[0]).toBeInTheDocument()
		window.history.back()
	})
})

test('Check Requirements - mic check failure, should redirect and display useful error message', () => {

	const mic_checked_routes: Array<string> = ["/setup-interview", "/pre-interview", "/interviewing"]

	mic_checked_routes.forEach(route => {
		window.history.pushState({}, 'Test page', route)
		render(<App />)
		expect(window.location.pathname.startsWith('/error/')).toBe(true)
		const elements = screen.getAllByText("Could not access microphone")
		expect(elements.length).toBeGreaterThan(0)
		expect(elements[0]).toBeInTheDocument()
		window.history.back()
	})
})

test('Check Requirements - mic check invalid, should not redirect on irrelevant routes', () => {

	const non_mic_checked_routes: Array<string> = ["/"]

	non_mic_checked_routes.forEach(route => {
		window.history.pushState({}, 'Test page', route)
		render(<App />)
		const elements = screen.queryAllByText("Could not access microphone")
		expect(elements.length).toEqual(0)
		window.history.back()
	})
})

test('Check Requirements - questions check failure, should redirect user and display useful error message', () => {
})