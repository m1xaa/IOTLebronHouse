package org.nba.lebronhouse.dto;

import org.nba.lebronhouse.state.AlarmState;

public record AlarmStateChangedDTO(
    String type,
    AlarmState state
) {
}
