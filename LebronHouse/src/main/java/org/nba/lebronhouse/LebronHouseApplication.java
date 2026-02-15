package org.nba.lebronhouse;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.integration.config.EnableIntegration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableIntegration
@EnableAsync
@EnableScheduling
public class LebronHouseApplication {

    public static void main(String[] args) {
        SpringApplication.run(LebronHouseApplication.class, args);
    }

}
