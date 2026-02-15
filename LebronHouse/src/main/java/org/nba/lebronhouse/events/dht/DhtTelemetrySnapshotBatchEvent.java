package org.nba.lebronhouse.events.dht;

import java.util.List;

public record DhtTelemetrySnapshotBatchEvent(
        List<DhtTelemetrySnapshotEvent> metrics
) {}

