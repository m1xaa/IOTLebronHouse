package org.nba.lebronhouse.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.AlarmStateChangedDTO;
import org.nba.lebronhouse.messaging.MqttPublisher;
import org.nba.lebronhouse.state.HouseState;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class DoorService {

    private final HouseState houseState;
    private final MqttPublisher mqttPublisher;
    private final ObjectMapper objectMapper;

    @Value("${mqtt.outbound.topic}")
    private String outboundTopic;

    public void handleLongPress() {
        boolean stateChanged = houseState.armAlarm();
        if (stateChanged)
            publish(true);
    }

    public void handleRelease() {
        boolean stateChanged = houseState.disarmAlarm();
        if (stateChanged)
            publish(false);
    }

    private void publish(boolean isArmed) {
        try {
            AlarmStateChangedDTO dto = new AlarmStateChangedDTO("alarm", isArmed);
            String json = objectMapper.writeValueAsString(dto);
            mqttPublisher.publish(outboundTopic, json);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Failed to serialize alarm state", e);
        }
    }
}
