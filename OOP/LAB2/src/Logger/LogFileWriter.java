package Logger;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class LogFileWriter {
    private static final SimpleDateFormat LOG_DATE_FORMAT = new SimpleDateFormat("[yyyy-MM-dd HH:mm:ss.SSS]");

    public static void main(String[] args) {
        createLogs("hi");
    }

    public static void createLogs(String interactionMessage) {
        String logMessage = generateUniqueIdentifier() + " " + getTimeInLogFormat() + " " + interactionMessage;
        writeLogToFile(logMessage);
    }

    private static String getTimeInLogFormat() {
        return LOG_DATE_FORMAT.format(new Date());
    }

    private static String generateUniqueIdentifier() {
        return System.getProperty("user.name") + "/" + System.getProperty("os.name");
    }

    private static void writeLogToFile(String content) {
        String filename = "app.log";
        try (FileWriter fileWriter = new FileWriter(filename, true);
             BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {

            bufferedWriter.write(content);
            bufferedWriter.newLine();

        } catch (IOException e) {
            System.out.println("An error occurred while writing to the log file.");
            e.printStackTrace();
        }
    }
}
