package org.nba.lebronhouse.events.btn;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.pi.SetSecondsIncrementDTO;
import org.nba.lebronhouse.dto.pi.SetTimerDTO;
import org.nba.lebronhouse.events.sd4.SetTimerEvent;
import org.nba.lebronhouse.messaging.MqttPublisher;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import tools.jackson.databind.ObjectMapper;

@Component
@RequiredArgsConstructor
public class SetSecondsIncrementListener {
    private final MqttPublisher mqttPublisher;
    private final ObjectMapper objectMapper;

    @Value("${mqtt.outbound.topic.PI2}")
    private String outboundTopic;

    @Async
    @EventListener
    public void handleSecondsIncrementChanged(SetSecondsIncrementEvent event) {
        SetSecondsIncrementDTO dto = new SetSecondsIncrementDTO("BTN", event.seconds());
        String json = objectMapper.writeValueAsString(dto);
        mqttPublisher.publish(outboundTopic, json);
    }
}

