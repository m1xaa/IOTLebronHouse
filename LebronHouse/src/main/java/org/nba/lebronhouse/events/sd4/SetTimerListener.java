package org.nba.lebronhouse.events.sd4;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.pi.DhtTelemetrySnapshotDTO;
import org.nba.lebronhouse.dto.pi.SetTimerDTO;
import org.nba.lebronhouse.events.dht.DhtTelemetrySnapshotBatchEvent;
import org.nba.lebronhouse.messaging.MqttPublisher;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import tools.jackson.databind.ObjectMapper;

@Component
@RequiredArgsConstructor
public class SetTimerListener {
    private final MqttPublisher mqttPublisher;
    private final ObjectMapper objectMapper;

    @Value("${mqtt.outbound.topic.PI2}")
    private String outboundTopic;

    @Async
    @EventListener
    public void handleSetTimer(SetTimerEvent event) {
        SetTimerDTO dto = new SetTimerDTO("SD4", event.seconds());
        String json = objectMapper.writeValueAsString(dto);
        mqttPublisher.publish(outboundTopic, json);
    }
}
