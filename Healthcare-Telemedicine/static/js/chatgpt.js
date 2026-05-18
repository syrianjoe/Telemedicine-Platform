let chatGPTInterface = {
    sendMessage: async function() {
        const input = document.getElementById('chatgptInput');
        const message = input.value.trim();
        if (!message) return;

        this.addMessage(message, 'user');

        try {
            const response = await fetch('/chatbot/api/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken') 
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            this.addMessage(data.response, 'bot');
        } catch (error) {
            console.error('Error:', error);
        }
    },
    getCookie: function(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    addMessage: function(text, sender) {
        const container = document.getElementById('chatgptMessages');
        const div = document.createElement('div');
        div.className = sender + '-message';
        div.innerText = text;
        container.appendChild(div);
    }
};