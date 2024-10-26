var textarea = document.getElementById('textarea');
var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
var recognition = new SpeechRecognition();
var listening = false; // Flag to control speech recognition loop

function inString(check, main) {
    return main.toLowerCase().includes(check);
}

function getAudio() {
    return new Promise((resolve) => {
        recognition.start();
        recognition.onresult = function (event) {
            var transcript = event.results[0][0].transcript;
            textarea.innerHTML = transcript;
            resolve(transcript.toLowerCase());
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
            textarea.innerHTML = 'Error occurred in recognition: ' + event.error;
            resolve(''); // Resolve with empty string on error
        };
    });
}

function speakText(text) {
    var speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
}

async function nova() {
    listening = true;
    const textarea = document.getElementById('textarea');

    while (listening) {
        let user_text = "";

        // Inner loop for speech recognition until 'nova' is heard
        while (true) {
            user_text = await getAudio();

            // If speech recognition returns empty (error or silence), continue to listen
            if (!user_text) {
                continue; // Repeat the loop to listen again
            }

            // Check if "nova" is in the user_text
            if (inString("nova", user_text)) {
                console.log("User said Nova, breaking out of first loop");
                break; // Break out of the inner loop if "nova" is found
            }
        }

        // Indicate analysis to user
        textarea.innerHTML = "Analyzing...";
        console.log("Analyzing text");

        // Stop recognition to prevent interruption while processing
        recognition.stop();

        // Process the voice input
        fetch('/process_voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_text: user_text })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response from Nova:", data.response);

            // Speak the response from Nova
            speakText(data.response);
            textarea.textContent = "Nova Is Speaking...";

            // Wait until Nova finishes speaking, then reset for next input
            speechSynthesis.onend = () => {
                textarea.textContent = "Say Nova's name with a question to activate";
                recognition.start(); // Restart recognition after speaking
            };
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function goToNova() {
    window.location.href = '/nova';
    speakText("Welcome To Nova A.I. Let's explore the cosmos together.");
}

function explore() {
    document.getElementById("explore-button").style.display = "none";
    document.getElementById("land-button").style.display = "flex";
    document.getElementById('textarea').textContent = "Say Nova With A Question To Activate";
    nova();
}

function land() {
    recognition.stop();
    document.getElementById("textarea").textContent = "Click Explore";
    document.getElementById("explore-button").style.display = "flex";
    document.getElementById("land-button").style.display = "none";
}