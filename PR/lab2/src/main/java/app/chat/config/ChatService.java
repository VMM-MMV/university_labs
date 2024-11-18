package app.chat.config;

import app.chat.components.ChatMessage;
import app.chat.components.MessageType;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.simp.SimpMessageSendingOperations;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class ChatService {
    private final SimpMessageSendingOperations messagingTemplate;

    public void broadcastUserLeftMessage(String username) {
        var chatMessage = ChatMessage.builder()
                .type(MessageType.LEAVE)
                .sender(username)
                .content(username + " has left the chat")
                .build();
        messagingTemplate.convertAndSend("/topic/public", chatMessage);
    }
}