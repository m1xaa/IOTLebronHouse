package org.nba.lebronhouse.messaging;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.write.Point;
import org.nba.lebronhouse.service.SensorEventService;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.messaging.MessageHandler;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;

import java.util.Iterator;
import java.util.Map;

@Service
public class MqttListener {

    private final InfluxDBClient influxDBClient;
    private final ObjectMapper objectMapper;
    private final SensorEventService sensorEventService;

    @Value("${influx.bucket}")
    private String bucket;

    @Value("${influx.org}")
    private String org;

    public MqttListener(InfluxDBClient influxDBClient, SensorEventService sensorEventService) {
        this.influxDBClient = influxDBClient;
        this.objectMapper = new ObjectMapper();
        this.sensorEventService = sensorEventService;
    }

    @Bean
    @ServiceActivator(inputChannel = "mqttInputChannel")
    public MessageHandler handler() {
        return message -> {
            try {
                String payload = message.getPayload().toString();

                JsonNode root = objectMapper.readTree(payload);
                String piId = root.path("pi_id").asText("unknown");


                if (root.has("batch")) {
                    for (JsonNode item : root.get("batch")) {

                        String component = item.get("component").asText();
                        boolean simulated = item.get("is_simulated").asBoolean();
                        JsonNode valueNode = item.get("value");

                        Point point = Point
                                .measurement(component)
                                .addTag("pi_id", piId)
                                .addTag("simulated", String.valueOf(simulated));

                        if (valueNode.isNumber()) {
                            point.addField("value", valueNode.doubleValue());
                        } else if (valueNode.isBoolean()) {
                            point.addField("value", valueNode.asBoolean());
                        } else if (valueNode.isObject()) {
                            Iterator<Map.Entry<String, JsonNode>> fields = valueNode.fields();

                            while (fields.hasNext()) {
                                Map.Entry<String, JsonNode> entry = fields.next();

                                if (entry.getValue().isNumber()) {
                                    point.addField(entry.getKey(), entry.getValue().doubleValue());
                                } else if (entry.getValue().isBoolean()) {
                                    point.addField(entry.getKey(), entry.getValue().asBoolean());
                                } else {
                                    point.addField(entry.getKey(), entry.getValue().asText());
                                }
                            }
                        } else {
                            point.addField("value", valueNode.asText());
                        }

                        influxDBClient.getWriteApiBlocking()
                                .writePoint(bucket, org, point);

                        sensorEventService.handleEvent(piId, component, simulated, valueNode);

//                        System.out.println("Saved: " + component);
                    }
                }

            } catch (Exception e) {
                System.out.println("Error processing MQTT message: " + e.getMessage());
            }
        };
    }
}
