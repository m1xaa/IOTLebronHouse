package org.nba.lebronhouse.service;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.QueryApi;
import com.influxdb.query.FluxRecord;
import com.influxdb.query.FluxTable;
import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.config.InfluxConfig;
import org.nba.lebronhouse.events.dht.DhtTelemetrySnapshotBatchEvent;
import org.nba.lebronhouse.events.dht.DhtTelemetrySnapshotEvent;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
@RequiredArgsConstructor
public class DhtTelemetrySnapshotProducer {

    private final InfluxDBClient influxDBClient;
    private final InfluxConfig influxConfig;
    private final ApplicationEventPublisher eventPublisher;

    @Scheduled(fixedRate = 10_000)
    public void produceSnapshot() {

        String flux = """
            from(bucket: "%s")
              |> range(start: -5m)
              |> filter(fn: (r) => r["_measurement"] == "DHT1"
                                  or r["_measurement"] == "DHT2"
                                  or r["_measurement"] == "DHT3")
              |> filter(fn: (r) => r["_field"] == "temperature"
                                  or r["_field"] == "humidity")
              |> last()
            """.formatted(influxConfig.getBucket());

        QueryApi queryApi = influxDBClient.getQueryApi();
        List<FluxTable> tables = queryApi.query(flux);

        Map<String, Map<String, Double>> grouped = new HashMap<>();

        for (FluxTable table : tables) {
            for (FluxRecord record : table.getRecords()) {

                String measurement = record.getMeasurement();
                String field = (String) record.getValueByKey("_field");
                Double value = ((Number) record.getValue()).doubleValue();

                grouped
                        .computeIfAbsent(measurement, k -> new HashMap<>())
                        .put(field, value);
            }
        }

        List<DhtTelemetrySnapshotEvent> metrics = new ArrayList<>();

        for (Map<String, Double> fields : grouped.values()) {
            Double temperature = fields.get("temperature");
            Double humidity = fields.get("humidity");

            if (temperature != null && humidity != null) {
                metrics.add(new DhtTelemetrySnapshotEvent(temperature, humidity));
            }
        }

        if (!metrics.isEmpty()) {
            eventPublisher.publishEvent(new DhtTelemetrySnapshotBatchEvent(metrics));
        }
    }
}
