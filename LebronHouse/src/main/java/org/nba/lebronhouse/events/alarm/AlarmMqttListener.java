package org.nba.lebronhouse.events.alarm;


import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.AlarmStateChangedDTO;
import org.nba.lebronhouse.messaging.MqttPublisher;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import tools.jackson.databind.ObjectMapper;

@Component
@RequiredArgsConstructor
public class AlarmMqttListener {

    private final MqttPublisher mqttPublisher;
    private final ObjectMapper objectMapper;

    @Value("${mqtt.outbound.topic}")
    private String outboundTopic;

    @Async
    @EventListener
    public void handleAlarmStateChanged(AlarmStateChangedEvent event) {
        AlarmStateChangedDTO dto = new AlarmStateChangedDTO("ALARM", event.state());
        String json = objectMapper.writeValueAsString(dto);
        mqttPublisher.publish(outboundTopic, json);
    }
}
