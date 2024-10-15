import { useLocation } from 'react-router-dom'

function Error() {

	const location = useLocation()
	const params = new URLSearchParams(location.search)
	const error_msgs = params.getAll('error_msg')

	return (
		<div>
			<h1>Error(s)</h1>

			<ul className="my-8">
				{error_msgs.map((msg, index) => (
					<li key={index} className="list-disc my-2">{msg}</li>
				))}
			</ul>
		</div>
	)
}

export default Error