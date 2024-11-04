package crazy;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/content")
public class DocsController {

    @Autowired
    private DocsService docsService;

    @PostMapping
    public void handleRequest(@RequestBody Map<String, String> request) {
        String content = request.get("content");
        String type = request.get("type");
        Request customRequest = new Request(content, type);
        docsService.addToQueue(customRequest);
    }
}
