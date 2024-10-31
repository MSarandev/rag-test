function createResponse(actor, message) {
    const chatBox = document.querySelector('.chat-box');
    const newMessage = document.createElement('div');

    newMessage.classList.add('message');
    newMessage.innerHTML = `<strong>${actor}:</strong> ${message}`;

    chatBox.appendChild(newMessage);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

document.getElementById('chat-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const spinner = document.getElementById('loading-spinner');
    const message = document.getElementById('question_input').value;

    createResponse("You", message);
    spinner.style.display = 'inline-block'; // Show the spinner


    fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"question_text": message})
    })
        .then(response => response.json())
        .then(data => {
            console.log('Received response (200)');

            createResponse("AI", data.response);
        })
        .catch((error) => {
            console.error('Error:', error);
        })
        .finally(() => {
            spinner.style.display = 'none'; // Hide the spinner
        });

    document.getElementById('question_input').value = ''; // Clear the input field
});