package org.nba.lebronhouse.dto;

import org.nba.lebronhouse.events.dht.DhtTelemetrySnapshotEvent;

import java.util.List;

public record DhtTelemetrySnapshotDTO(
        String type,
        List<DhtTelemetrySnapshotEvent> metrics
) {
}
