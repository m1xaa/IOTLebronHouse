package org.nba.lebronhouse.dto;

public record AlarmStateChangedDTO(
    String type,
    boolean isArmed
) {
}
