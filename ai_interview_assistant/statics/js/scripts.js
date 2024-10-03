const socket = io();

// Elements
const startButton = document.getElementById('start-interview');
const avatarCanvas = document.getElementById('avatar-canvas');

let mediaRecorder;
let audioChunks = [];

// Function to play TTS audio
function playAudio(audioBase64) {
    const audioData = base64ToArrayBuffer(audioBase64);
    const blob = new Blob([audioData], { type: 'audio/mpeg' });
    const audioUrl = URL.createObjectURL(blob);
    const audio = new Audio(audioUrl);
    audio.play();
    return audio;
}

// Utility function to convert base64 to ArrayBuffer
function base64ToArrayBuffer(base64) {
    const binaryString = window.atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++)        {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}

// Function to start the interview
startButton.addEventListener('click', () => {
    startButton.disabled = true;
    askQuestion();
});

function askQuestion() {
    socket.emit('get_audio', {});
}

// Handle TTS audio from server
socket.on('play_audio', (data) => {
    const audio = playAudio(data.audio);
    audio.onended = () => {
        // Start recording candidate's response
        startRecording();
    };
});

socket.on('evaluation_complete', () => {
    // Proceed to next question
    askQuestion();
});

socket.on('interview_complete', () => {
    // Interview is over
    alert('Interview complete. Thank you for your time.');
    // Optionally redirect or perform another action
});

// Function to start recording
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            audioChunks = [];
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm; codecs=opus' });
                const reader = new FileReader();
                reader.onloadend = () => {
                    const base64data = reader.result.split(',')[1];
                    socket.emit('audio_data', { audio: base64data });
                };
                reader.readAsDataURL(audioBlob);
            };
            mediaRecorder.start();

            // Stop recording after predefined time (e.g., 2 minutes)
            setTimeout(() => {
                mediaRecorder.stop();
            }, 120000); // 2 minutes
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
}
