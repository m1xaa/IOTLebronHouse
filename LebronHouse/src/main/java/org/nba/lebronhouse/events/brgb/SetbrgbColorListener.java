package org.nba.lebronhouse.events.brgb;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.pi.BrgbColorChangedDTO;
import org.nba.lebronhouse.dto.pi.DhtTelemetrySnapshotDTO;
import org.nba.lebronhouse.events.dht.DhtTelemetrySnapshotBatchEvent;
import org.nba.lebronhouse.messaging.MqttPublisher;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import tools.jackson.databind.ObjectMapper;

@Component
@RequiredArgsConstructor
public class SetbrgbColorListener {

    private final MqttPublisher mqttPublisher;
    private final ObjectMapper objectMapper;

    @Value("${mqtt.outbound.topic.PI3}")
    private String outboundTopic;

    @Async
    @EventListener
    public void handleBrgbColorChanged(SetBrgbColorEvent event) {
        BrgbColorChangedDTO dto = new BrgbColorChangedDTO("BRGB", event.red(), event.green(), event.blue());
        String json = objectMapper.writeValueAsString(dto);
        mqttPublisher.publish(outboundTopic, json);
    }
}
