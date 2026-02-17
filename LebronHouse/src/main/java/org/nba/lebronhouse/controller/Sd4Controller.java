package org.nba.lebronhouse.controller;

import lombok.RequiredArgsConstructor;
import okhttp3.Response;
import org.nba.lebronhouse.dto.requests.SetSecondsIncrementRequest;
import org.nba.lebronhouse.dto.requests.SetTimerRequest;
import org.nba.lebronhouse.service.Sd4Service;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/api/sd4")
@RequiredArgsConstructor
public class Sd4Controller {

    private final Sd4Service service;

    @PutMapping("/timer")
    public ResponseEntity<Void> setTimer(@RequestBody SetTimerRequest request) {
        service.setTimer(request);
        return ResponseEntity.ok().build();
    }

    @PutMapping("/seconds")
    public ResponseEntity<Void> setSecondsIncrement(@RequestBody SetSecondsIncrementRequest request) {
        service.setSecondsIncrement(request);
        return ResponseEntity.ok().build();
    }
}
