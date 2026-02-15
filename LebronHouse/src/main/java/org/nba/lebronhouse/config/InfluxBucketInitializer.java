package org.nba.lebronhouse.config;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.domain.Bucket;
import com.influxdb.client.domain.BucketRetentionRules;
import com.influxdb.client.domain.Organization;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Collections;

@Component
@RequiredArgsConstructor
public class InfluxBucketInitializer {

    private final InfluxDBClient influxDBClient;

    @Value("${influx.bucket}")
    private String bucketName;

    @Value("${influx.org}")
    private String orgName;

    @PostConstruct
    public void ensureBucketExists() {

        var bucketsApi = influxDBClient.getBucketsApi();
        var orgApi = influxDBClient.getOrganizationsApi();

        Organization org = orgApi.findOrganizations()
                .stream()
                .filter(o -> o.getName().equals(orgName))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("Org not found: " + orgName));

        Bucket existing = bucketsApi.findBucketByName(bucketName);

        if (existing == null) {
            bucketsApi.createBucket(bucketName, org);
            System.out.println("Created bucket: " + bucketName);
        } else {
            System.out.println("Bucket already exists: " + bucketName);
        }
    }
}
