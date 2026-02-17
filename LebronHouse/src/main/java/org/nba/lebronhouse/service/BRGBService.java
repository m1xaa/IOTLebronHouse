package org.nba.lebronhouse.service;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.requests.SetBrgbColorRequest;
import org.nba.lebronhouse.events.brgb.SetBrgbColorEvent;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class BRGBService {

    private final ApplicationEventPublisher eventPublisher;

    public void setBRGBColor(SetBrgbColorRequest request) {
        eventPublisher.publishEvent(
                new SetBrgbColorEvent(request.red(), request.green(), request.blue())
        );
    }
}
