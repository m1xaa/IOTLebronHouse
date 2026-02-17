package org.nba.lebronhouse.controller;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.events.alarm.AlarmStateChangedEvent;
import org.nba.lebronhouse.state.AlarmState;
import org.nba.lebronhouse.state.HouseState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/api/alarm")
@RequiredArgsConstructor
public class AlarmController {

    private final HouseState houseState;
    private final ApplicationEventPublisher eventPublisher;


    @GetMapping("/state")
    public ResponseEntity<AlarmState> getCurrentState() {
        return ResponseEntity.ok(houseState.getAlarmState());
    }

    @PostMapping("/state/{state}")
    public ResponseEntity<Void> changeState(@PathVariable AlarmState state) {
        switch (state) {
            case AlarmState.DISARMED, AlarmState.ARMED -> {
                houseState.clearAlarmReasons();
            }
            case AlarmState.ALARM -> {
                houseState.addAlarmReason("WEB");
            }

            case AlarmState.ARMING -> {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
            }
        }
        boolean stateChanged = houseState.setState(state);
        if (stateChanged) {
            eventPublisher.publishEvent(new AlarmStateChangedEvent(state));
        }
        return ResponseEntity.ok().build();
    }
}

