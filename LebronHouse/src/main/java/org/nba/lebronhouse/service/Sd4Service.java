package org.nba.lebronhouse.service;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.requests.SetSecondsIncrementRequest;
import org.nba.lebronhouse.dto.requests.SetTimerRequest;
import org.nba.lebronhouse.events.btn.SetSecondsIncrementEvent;
import org.nba.lebronhouse.events.sd4.SetTimerEvent;
import org.nba.lebronhouse.state.HouseState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class Sd4Service {

    private final ApplicationEventPublisher eventPublisher;
    private final HouseState houseState;

    public void setTimer(SetTimerRequest request) {
        eventPublisher.publishEvent(new SetTimerEvent(request.seconds()));
    }

    public void setSecondsIncrement(SetSecondsIncrementRequest request) {
        houseState.setSecondsIncrement(request.seconds());
        eventPublisher.publishEvent(new SetSecondsIncrementEvent(request.seconds()));
    }

    public int getSecondsIncrement() {
        return houseState.getSecondsIncrement();
    }
}
