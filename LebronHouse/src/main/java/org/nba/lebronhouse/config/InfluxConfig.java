package org.nba.lebronhouse.config;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.InfluxDBClientFactory;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class InfluxConfig {

    @Value("${influx.url}")
    private String url;

    @Value("${influx.token}")
    private String token;

    @Getter
    @Value("${influx.org}")
    private String org;

    @Getter
    @Value("${influx.bucket}")
    private String bucket;

    @Bean
    public InfluxDBClient influxDBClient() {
        return InfluxDBClientFactory.create(url, token.toCharArray(), org);
    }

}

