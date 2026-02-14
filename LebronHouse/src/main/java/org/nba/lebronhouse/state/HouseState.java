package org.nba.lebronhouse.state;


import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

@Component
public class HouseState {

    private final AtomicReference<AlarmState> alarmState =
            new AtomicReference<>(AlarmState.DISARMED);
    private final AtomicInteger personsInside = new AtomicInteger(0);
    private final AtomicInteger extraSeconds = new AtomicInteger(15);


    public AlarmState getAlarmState() {
        return alarmState.get();
    }

    public void setAlarmState(AlarmState newState) {
        alarmState.set(newState);
    }



    public int getPersonsInside() {
        return personsInside.get();
    }

    public void incrementPersons() {
        personsInside.incrementAndGet();
    }

    public void decrementPersons() {
        personsInside.decrementAndGet();
    }



    public int getExtraSeconds() {
        return extraSeconds.get();
    }

    public void setExtraSeconds(int seconds) {
        extraSeconds.set(seconds);
    }
}
