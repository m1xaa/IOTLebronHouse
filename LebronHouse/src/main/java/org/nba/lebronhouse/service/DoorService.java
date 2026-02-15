package org.nba.lebronhouse.service;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.config.HouseConfig;
import org.nba.lebronhouse.events.alarm.AlarmStateChangedEvent;
import org.nba.lebronhouse.state.AlarmState;
import org.nba.lebronhouse.state.HouseState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@Service
@RequiredArgsConstructor
public class DoorService {

    private final HouseState houseState;
    private final HouseConfig houseConfig;
    private final ApplicationEventPublisher eventPublisher;

    private final ScheduledExecutorService scheduler =
            Executors.newSingleThreadScheduledExecutor();

    public void doorUnlocked() {
        boolean stateChanged = houseState.armAlarm();
        if (stateChanged)
            eventPublisher.publishEvent(new AlarmStateChangedEvent(AlarmState.ALARM));
    }

    public void doorLocked() {
        boolean stateChanged = houseState.disarmAlarm();
        if (stateChanged)
            eventPublisher.publishEvent(new AlarmStateChangedEvent(AlarmState.DISARMED));
    }

    public void doorActionDetected() {
        AlarmState current = houseState.getAlarmState();
        if (current != AlarmState.ARMED)
            return;
        houseState.setState(AlarmState.ALARM);
        eventPublisher.publishEvent(new AlarmStateChangedEvent(AlarmState.ALARM));
    }

    public void verifyPin(String pin) {

        if (!houseConfig.getPin().equals(pin))
            return;

        AlarmState current = houseState.getAlarmState();

        if (current == AlarmState.DISARMED) {

            boolean changed = houseState.setState(AlarmState.ARMING);
            if (changed)
                eventPublisher.publishEvent(
                        new AlarmStateChangedEvent(AlarmState.ARMING)
                );

            scheduler.schedule(() -> {
                if (houseState.getAlarmState() == AlarmState.ARMING) {
                    boolean armedChanged =
                            houseState.setState(AlarmState.ARMED);

                    if (armedChanged)
                        eventPublisher.publishEvent(
                                new AlarmStateChangedEvent(AlarmState.ARMED)
                        );
                }
            }, 10, TimeUnit.SECONDS);

        } else {
            boolean changed = houseState.setState(AlarmState.DISARMED);
            if (changed)
                eventPublisher.publishEvent(
                        new AlarmStateChangedEvent(AlarmState.DISARMED)
                );
        }
    }


}
