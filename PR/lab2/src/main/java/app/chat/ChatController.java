package app.chat;

import app.chat.components.ChatMessage;
import app.chat.config.ChatService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;

import java.util.Optional;

@Controller
@Slf4j
@RequiredArgsConstructor
@Validated
public class ChatController {
    private final ChatService chatService;

    @MessageMapping("/chat.sendMessage")
    @SendTo("/topic/public")
    public ChatMessage sendMessage(@Payload ChatMessage chatMessage) {
        return chatMessage;
    }

    @MessageMapping("/chat.addUser")
    @SendTo("/topic/public")
    public ChatMessage addUser(
            @Payload ChatMessage chatMessage,
            SimpMessageHeaderAccessor headerAccessor) {

        Optional.ofNullable(headerAccessor.getSessionAttributes())
                .orElseThrow(() -> new IllegalStateException("Session attributes cannot be null"));

        headerAccessor.getSessionAttributes().put("username", chatMessage.getSender());
        log.info("User added to chat: {}", chatMessage.getSender());
        return chatMessage;
    }
}