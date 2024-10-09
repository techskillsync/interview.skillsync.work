import { Link, useLocation } from 'react-router-dom'
import { FaPlay } from "react-icons/fa";

function PreInterview() {
	const location = useLocation()

    return (
		<div className="flex flex-col justify-center items-center">
			<h1>You will be interviewing with <b className="text-[#a745d6]">Rachel</b>,<br/>
			    click the play button to begin. </h1>
			<Link to={{ pathname: "/interviewing", search: location.search }}>
					<FaPlay size={36} color='#a745d6' className="m-8" />
			</Link>
		</div>
	)
}

export default PreInterview