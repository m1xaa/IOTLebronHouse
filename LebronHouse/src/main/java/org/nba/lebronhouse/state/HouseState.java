package org.nba.lebronhouse.state;


import org.springframework.stereotype.Component;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

@Component
public class HouseState {

    private final AtomicReference<AlarmState> alarmState =
            new AtomicReference<>(AlarmState.DISARMED);
    private final AtomicInteger personInside = new AtomicInteger(0);
    private final AtomicInteger extraSeconds = new AtomicInteger(15);

    private final Set<String> alarmReasons = ConcurrentHashMap.newKeySet();


    public AlarmState getAlarmState() {
        return alarmState.get();
    }

    public boolean setState(AlarmState newState) {
        AlarmState previous = alarmState.getAndSet(newState);
        return previous != newState;
    }


    public boolean armAlarm() {
        AlarmState previous = alarmState.getAndSet(AlarmState.ALARM);
        return previous != AlarmState.ALARM;
    }

    public boolean disarmAlarm() {
        AlarmState previous = alarmState.getAndSet(AlarmState.DISARMED);
        return previous != AlarmState.DISARMED;
    }


    public int getPersonInside() {
        return personInside.get();
    }

    public void incrementPerson() {
        personInside.incrementAndGet();
    }

    public void decrementPerson() {
        personInside.updateAndGet(current ->
                current > 0 ? current - 1 : 0
        );
    }


    public int getExtraSecond() {
        return extraSeconds.get();
    }

    public void setExtraSeconds(int seconds) {
        extraSeconds.set(seconds);
    }


    public boolean addAlarmReason(String reason) {
        return alarmReasons.add(reason);
    }

    public boolean removeAlarmReason(String reason) {
        return alarmReasons.remove(reason);
    }

    public void clearAlarmReasons() {
        alarmReasons.clear();
    }

    public boolean hasAlarmReasons() {
        return !alarmReasons.isEmpty();
    }

    public Set<String> getAlarmReasons() {
        return Set.copyOf(alarmReasons);
    }
}
