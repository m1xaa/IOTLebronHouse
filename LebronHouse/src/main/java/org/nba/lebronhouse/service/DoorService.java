package org.nba.lebronhouse.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.AlarmStateChangedDTO;
import org.nba.lebronhouse.events.alarm.AlarmStateChangedEvent;
import org.nba.lebronhouse.messaging.MqttPublisher;
import org.nba.lebronhouse.state.AlarmState;
import org.nba.lebronhouse.state.HouseState;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class DoorService {

    private final HouseState houseState;
    private final ApplicationEventPublisher eventPublisher;

    public void handleLongPress() {
        boolean stateChanged = houseState.armAlarm();
        if (stateChanged)
            eventPublisher.publishEvent(new AlarmStateChangedEvent(AlarmState.ALARM));
    }

    public void handleRelease() {
        boolean stateChanged = houseState.disarmAlarm();
        if (stateChanged)
            eventPublisher.publishEvent(new AlarmStateChangedEvent(AlarmState.DISARMED));
    }

}
