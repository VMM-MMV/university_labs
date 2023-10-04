package Logging;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Logger {
    String fileName;
    public Logger(String inputedFileName) {
        fileName = inputedFileName;
    }
    public Logger() {
        fileName = "app.log";
    }
    private final SimpleDateFormat LOG_DATE_FORMAT = new SimpleDateFormat("[yyyy-MM-dd HH:mm:ss.SSS]");

    public void log(String interactionMessage) {
        String logMessage = generateUniqueIdentifier() + " " + getTimeInLogFormat() + " " + interactionMessage;
        writeLogToFile(logMessage);
    }

    private String getTimeInLogFormat() {
        return LOG_DATE_FORMAT.format(new Date());
    }

    private String generateUniqueIdentifier() {
        return System.getProperty("user.name") + "/" + System.getProperty("os.name");
    }

    private void writeLogToFile(String content) {
        try (FileWriter fileWriter = new FileWriter(fileName, true);
             BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {

            bufferedWriter.write(content);
            bufferedWriter.newLine();

        } catch (IOException e) {
            System.out.println("An error occurred while writing to the log file.");
            e.printStackTrace();
        }
    }
}
