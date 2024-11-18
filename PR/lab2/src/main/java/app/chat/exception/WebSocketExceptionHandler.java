package app.chat.exception;

import jakarta.validation.ConstraintViolationException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.handler.annotation.MessageExceptionHandler;
import org.springframework.messaging.simp.annotation.SendToUser;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.MethodArgumentNotValidException;

import java.util.stream.Collectors;

@Controller
@Slf4j
public class WebSocketExceptionHandler {
    public record ErrorResponse(String type, String message) {}

    @MessageExceptionHandler(MethodArgumentNotValidException.class)
    @SendToUser("/queue/errors")
    public ErrorResponse handleMethodArgumentNotValidException(MethodArgumentNotValidException exception) {
        log.error("Validation error occurred", exception);

        String errorMessage = exception.getBindingResult().getFieldErrors().stream()
                .map(error -> error.getField() + ": " + error.getDefaultMessage())
                .collect(Collectors.joining(", "));

        return new ErrorResponse("Validation Error", errorMessage);
    }

    @MessageExceptionHandler(ConstraintViolationException.class)
    @SendToUser("/queue/errors")
    public ErrorResponse handleConstraintViolationException(ConstraintViolationException exception) {
        log.error("Constraint violation error occurred", exception);
        return new ErrorResponse("Constraint Violation", exception.getMessage());
    }

    @MessageExceptionHandler({Exception.class, RuntimeException.class})
    @SendToUser("/queue/errors")
    public ErrorResponse handleGenericException(Exception exception) {
        log.error("Unexpected error occurred", exception);
        return new ErrorResponse("Unexpected Error", exception.getMessage());
    }
}