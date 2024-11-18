package app.chat.config;

import app.chat.components.ChatMessage;
import app.chat.components.MessageType;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.event.EventListener;
import org.springframework.messaging.simp.SimpMessageSendingOperations;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.messaging.SessionDisconnectEvent;

import java.util.Optional;

@Slf4j
@Component
@RequiredArgsConstructor
public class WebSocketEventListener {
    private final ChatService chatService;

    @EventListener
    public void handleWebSocketDisconnectListener(SessionDisconnectEvent event) {
        StompHeaderAccessor headerAccessor = StompHeaderAccessor.wrap(event.getMessage());

        Optional.ofNullable(headerAccessor.getSessionAttributes())
                .map(attrs -> (String) attrs.get("username"))
                .ifPresentOrElse(
                        chatService::broadcastUserLeftMessage,
                        () -> log.warn("Disconnected session with no username")
                );
    }
}