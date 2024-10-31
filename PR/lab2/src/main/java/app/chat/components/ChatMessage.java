package app.chat.components;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ChatMessage {
    @NotNull(message = "Message type cannot be null")
    private MessageType type;

    @NotBlank(message = "Content cannot be blank")
    private String content;

    @NotBlank(message = "Sender cannot be blank")
    private String sender;
}