package org.nba.lebronhouse.events.alarm;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.WriteApi;
import com.influxdb.client.domain.WritePrecision;
import com.influxdb.client.write.Point;
import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.config.InfluxConfig;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import java.time.Instant;

@Component
@RequiredArgsConstructor
public class AlarmMetricsListener {

    private final InfluxDBClient influxDBClient;
    private final InfluxConfig influxConfig;

    @Async
    @EventListener
    public void handleAlarmStateChanged(AlarmStateChangedEvent event) {

        Point point = Point
                .measurement("ALARM")
                .addField("state", event.state().ordinal())
                .time(Instant.now(), WritePrecision.MS);

        try (WriteApi writeApi = influxDBClient.getWriteApi()) {
            writeApi.writePoint(influxConfig.getBucket(), influxConfig.getOrg(), point);
        }
    }
}
