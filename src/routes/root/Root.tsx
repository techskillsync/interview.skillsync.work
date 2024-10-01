import { Link } from 'react-router-dom'
import { FaPlay } from "react-icons/fa";

function Root() {
    return (
		<div className="flex flex-col justify-center items-center">
			<h1>You will be interviewing with <b className="text-[#1D7547]">Callum</b>,<br/>
			    click the play button to begin. </h1>
			<Link to="interviewing"><FaPlay size={36} color='#1D7547' className="m-8" /></Link>
		</div>
	)
}

export default Root;