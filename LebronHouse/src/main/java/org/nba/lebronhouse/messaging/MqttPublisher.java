package org.nba.lebronhouse.messaging;

import lombok.RequiredArgsConstructor;
import org.springframework.integration.support.MessageBuilder;
import org.springframework.messaging.MessageChannel;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class MqttPublisher {

    private final MessageChannel mqttOutboundChannel;

    public void publish(String topic, String payload) {
        mqttOutboundChannel.send(
                MessageBuilder
                        .withPayload(payload)
                        .setHeader("mqtt_topic", topic)
                        .build()
        );
    }
}