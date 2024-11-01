'use strict';

const loginPage = document.querySelector('#login-page');
const chatPage = document.querySelector('#chat-page');
const loginForm = document.querySelector('#login-form');
const messageForm = document.querySelector('#messageForm');
const messageInput = document.querySelector('#message');
const messageArea = document.querySelector('#messageArea');
const connectingElement = document.querySelector('.connecting');
const usernameDisplay = document.querySelector('#username');
const userAvatar = document.querySelector('#userAvatar');

let stompClient = null;
let username = null;

const colors = [
    '#2196F3', '#32c787', '#00BCD4', '#ff5652',
    '#ffc107', '#ff85af', '#FF9800', '#39bbb0'
];

function connect(event) {
    username = document.querySelector('#name').value.trim();

    if(username) {
        loginPage.classList.add('hidden');
        chatPage.classList.remove('hidden');

        usernameDisplay.textContent = username;
        userAvatar.textContent = username.charAt(0).toUpperCase();
        userAvatar.style.backgroundColor = getAvatarColor(username);

        const socket = new SockJS('/ws');
        stompClient = Stomp.over(socket);

        stompClient.connect({}, onConnected, onError);
    }
    event.preventDefault();
}

function logout() {
    if(stompClient) {
        stompClient.send("/app/chat.addUser",
            {},
            JSON.stringify({sender: username, type: 'LEAVE'})
        );
        stompClient.disconnect();
    }

    loginPage.classList.remove('hidden');
    chatPage.classList.add('hidden');
    messageArea.innerHTML = '';
    stompClient = null;
    username = null;

    document.querySelector('#name').value = '';
    document.querySelector('#name').focus();
}

function getAvatarColor(messageSender) {
    let hash = 0;
    for (let i = 0; i < messageSender.length; i++) {
        hash = 31 * hash + messageSender.charCodeAt(i);
    }
    const index = Math.abs(hash % colors.length);
    return colors[index];
}

function onConnected() {
    stompClient.subscribe('/topic/public', onMessageReceived);
    stompClient.send("/app/chat.addUser",
        {},
        JSON.stringify({sender: username, type: 'JOIN'})
    );
    connectingElement.classList.add('hidden');
}

function onError(error) {
    connectingElement.textContent = 'Could not connect to chat server. Please refresh and try again.';
    connectingElement.classList.remove('hidden');
    connectingElement.style.background = '#ff5652';
    connectingElement.style.color = 'white';
}

function sendMessage(event) {
    const messageContent = messageInput.value.trim();

    if(messageContent && stompClient) {
        const chatMessage = {
            sender: username,
            content: messageInput.value,
            type: 'CHAT'
        };
        stompClient.send("/app/chat.sendMessage", {}, JSON.stringify(chatMessage));
        messageInput.value = '';
    }
    event.preventDefault();
}

function onMessageReceived(payload) {
    const message = JSON.parse(payload.body);
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');

    if(message.type === 'JOIN') {
        messageElement.classList.add('system-message');
        messageElement.textContent = `${message.sender} joined the chat`;
    } else if (message.type === 'LEAVE') {
        messageElement.classList.add('system-message');
        messageElement.textContent = `${message.sender} left the chat`;
    } else {
        const isMyMessage = message.sender === username;
        messageElement.classList.add(isMyMessage ? 'sent' : 'received');

        const bubbleElement = document.createElement('div');
        bubbleElement.classList.add('message-bubble');
        bubbleElement.textContent = message.content;

        messageElement.appendChild(bubbleElement);
    }

    messageArea.appendChild(messageElement);
    messageArea.scrollTop = messageArea.scrollHeight;
}

loginForm.addEventListener('submit', connect, true);
messageForm.addEventListener('submit', sendMessage, true);

document.querySelector('#name').focus();

const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.target.id === 'chat-page' &&
            !mutation.target.classList.contains('hidden')) {
            messageInput.focus();
        }
    });
});

observer.observe(chatPage, { attributes: true });