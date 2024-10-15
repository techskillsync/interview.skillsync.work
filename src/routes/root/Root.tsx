import { Link, useLocation } from 'react-router-dom'
import { useMicAccess } from "../../components/MicAccessContext"

function Root() {
	const location = useLocation();
	const { has_mic_access } = useMicAccess()

	return (
		<div className="flex flex-col justify-center items-center">
			{has_mic_access ?
				<div>
					<h1>
						We detected your microphone! Make some noise to make sure its working
					</h1>
					<Link 
						to={{ pathname: "/setup-interview", search: location.search }}
						className="w-full my-4 flex justify-center items-center">
						<h1 className="block p-4 rounded-lg bg-[#1d754835] text-[#1d7547]">Its working</h1>
					</Link>
				</div>
				:
				<h1>
					Welcome, before we begin make sure we can detect your microphone
				</h1>
			}
		</div>
	)
}

export default Root;