package com.example.config;

import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
public class AppInfo {

    private final Environment environment;

    public AppInfo(Environment environment) {
        this.environment = environment;
    }

    public String getUrl() {
        String host = environment.getProperty("local.server.host");
        String port = environment.getProperty("local.server.port");
        return "http://" + host + "/" + port;
    }
}
