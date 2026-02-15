package org.nba.lebronhouse.service;

import com.influxdb.client.InfluxDBClient;
import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.config.InfluxConfig;
import org.nba.lebronhouse.events.alarm.AlarmStateChangedEvent;
import org.nba.lebronhouse.state.AlarmState;
import org.nba.lebronhouse.state.HouseState;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class MotionService {

    private final InfluxDBClient influxDBClient;
    private final InfluxConfig influxConfig;

    private final HouseState houseState;

    private final ApplicationEventPublisher eventPublisher;


    public void checkRecentMotion(String component) {

        String flux = String.format("""
        from(bucket: "%s")
          |> range(start: -15s)
          |> filter(fn: (r) => r._measurement == "%s")
          |> filter(fn: (r) => r._field == "value")
          |> sort(columns: ["_time"])
        """, influxConfig.getBucket(), component);

        List<Double> distances = new ArrayList<>();

        influxDBClient.getQueryApi().query(flux, influxConfig.getOrg()).forEach(table ->
                table.getRecords().forEach(record -> {
                    Object value = record.getValue();
                    if (value instanceof Number number) {
                        distances.add(number.doubleValue());
                    }
                })
        );

        if (distances.size() < 2) {
            return;
        }

        double first = distances.get(0);
        double last = distances.get(distances.size() - 1);

        if (last < first) {
            houseState.incrementPerson();
        } else if (last > first) {
            houseState.decrementPerson();
        }
    }

    public void motionDetected() {
        if (houseState.getPersonInside() > 0)
            return;
        AlarmState current = houseState.getAlarmState();
        if (!current.equals(AlarmState.ARMED))
            return;

        boolean stateChanged = houseState.setState(AlarmState.ALARM);
        if (stateChanged) {
            houseState.addAlarmReason("DPIR");
            eventPublisher.publishEvent(new AlarmStateChangedEvent(AlarmState.ALARM));
        }
    }

    public void handleGsgMovement() {
        AlarmState current = houseState.getAlarmState();
        if (!current.equals(AlarmState.ARMED))
            return;

        boolean stateChanged = houseState.setState(AlarmState.ALARM);
        if (stateChanged) {
            houseState.addAlarmReason("GSG");
            eventPublisher.publishEvent(new AlarmStateChangedEvent(AlarmState.ALARM));
        }
    }
}
