package org.nba.lebronhouse.dto.pi;

import org.nba.lebronhouse.state.AlarmState;

public record AlarmStateChangedDTO(
    String type,
    AlarmState state
) {
}
