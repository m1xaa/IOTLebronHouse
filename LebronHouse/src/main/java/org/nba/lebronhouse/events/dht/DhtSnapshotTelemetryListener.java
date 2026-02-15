package org.nba.lebronhouse.events.dht;


import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.DhtTelemetrySnapshotDTO;
import org.nba.lebronhouse.messaging.MqttPublisher;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import tools.jackson.databind.ObjectMapper;

import java.util.List;

@Component
@RequiredArgsConstructor
public class DhtSnapshotTelemetryListener {

    private final MqttPublisher mqttPublisher;
    private final ObjectMapper objectMapper;

    @Value("${mqtt.outbound.topic.PI3}")
    private String outboundTopic;

    @Async
    @EventListener
    public void handleAlarmStateChanged(DhtTelemetrySnapshotBatchEvent event) {
        DhtTelemetrySnapshotDTO dto = new DhtTelemetrySnapshotDTO("DHT", event.metrics());
        String json = objectMapper.writeValueAsString(dto);
        mqttPublisher.publish(outboundTopic, json);
    }
}
