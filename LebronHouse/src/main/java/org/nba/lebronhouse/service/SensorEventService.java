package org.nba.lebronhouse.service;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SensorEventService {

    private final MotionService motionService;
    private final DoorService doorService;

    public void handleEvent(String piId, String component, boolean simulated, JsonNode value) {

        switch (component) {
            case "DPIR1" -> {
                if (value.isBoolean() && value.asBoolean()) {
                    motionService.checkRecentMotion("DUS1");
                }
            }
            case "DPIR2" -> {
                if (value.isBoolean() && value.asBoolean()) {
                    motionService.checkRecentMotion("DUS2");
                }
            }

            case "DS1", "DS2" -> {
                if (!value.isTextual())
                    return;
                if (value.asText().equals("LONG_PRESS")) {
                    doorService.doorUnlocked();
                } else if (value.asText().equals("RELEASE")) {
                    doorService.doorLocked();
                }
                else {
                    doorService.doorActionDetected();
                }
            }

            case "DMS" -> {
                if (!value.isTextual())
                    return;
                doorService.verifyPin(value.asText());
            }
        }

    }
}

