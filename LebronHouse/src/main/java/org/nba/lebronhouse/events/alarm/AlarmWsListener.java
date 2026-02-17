package org.nba.lebronhouse.events.alarm;

import lombok.RequiredArgsConstructor;
import org.springframework.context.event.EventListener;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class AlarmWsListener {

    private final SimpMessagingTemplate messagingTemplate;

    @Async
    @EventListener
    public void handleAlarmStateChanged(AlarmStateChangedEvent event) {
        messagingTemplate.convertAndSend(
                "/topic/alarm",
                event.state()
        );
    }
}
