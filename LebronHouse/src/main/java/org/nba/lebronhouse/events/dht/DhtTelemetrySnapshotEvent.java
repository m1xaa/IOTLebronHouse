package org.nba.lebronhouse.events.dht;

public record DhtTelemetrySnapshotEvent(
    double temperature,
    double humidity
) { }
