/*
 * Records the user's audio while displaying a waveform indicator
 * so the user knows their audio is being picked up
 */

import { useRef } from "react";
import { useMicAccess } from "./MicAccessContext";

async function audioRecorder() 
{
	const mediaRecorderRef = useRef<MediaRecorder | null>(null);

	try {
		const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
		mediaRecorderRef.current = new MediaRecorder(stream);
		let chuncks = [];

		mediaRecorderRef.current.ondataavailable = function(event) {
			chuncks.push(event.data)
		}

		mediaRecorderRef.current.onstop = function () {
			console.log("Recording finished")
		}
	} catch (error) {
	}
}

function Microphone() {
	const { hasMicAccess } = useMicAccess()

	return(
		<div className="bg-sky-200 p-4 fixed bottom-24 left-1/2 transform -translate-x-1/2">
			{hasMicAccess ?
				<div>
					<button className="p-4 m-4 border">
						Stop recording and send to backend
					</button>
				</div>
				:
				<div>
					I dont have access :&#40;
				</div>
			}
		</div>
	)
}

export default Microphone