package org.nba.lebronhouse.events.alarm;

import org.nba.lebronhouse.state.AlarmState;

public record AlarmStateChangedEvent(
        AlarmState state
) {
}
