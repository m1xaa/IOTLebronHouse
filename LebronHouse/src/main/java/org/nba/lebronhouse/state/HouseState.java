package org.nba.lebronhouse.state;


import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

@Component
public class HouseState {

    private final AtomicBoolean alarmOn = new AtomicBoolean(false);
    private final AtomicInteger personsInside = new AtomicInteger(0);
    private final AtomicInteger extraSeconds = new AtomicInteger(15);


    public boolean isAlarmOn() {
        return alarmOn.get();
    }

    public void setAlarmOn(boolean value) {
        alarmOn.set(value);
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
