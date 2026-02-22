package org.nba.lebronhouse.events.motion;


import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.events.alarm.AlarmStateChangedEvent;
import org.springframework.context.event.EventListener;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class CheckRecentMotionListener {

    private final SimpMessagingTemplate messagingTemplate;

    @Async
    @EventListener
    public void handleRecentMotion(CheckRecentMotionEvent event) {
        messagingTemplate.convertAndSend(
                "/topic/motion",
                event.personCount()
        );
    }
}
