package org.nba.lebronhouse;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.integration.config.EnableIntegration;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableIntegration
@EnableAsync
public class LebronHouseApplication {

    public static void main(String[] args) {
        SpringApplication.run(LebronHouseApplication.class, args);
    }

}
