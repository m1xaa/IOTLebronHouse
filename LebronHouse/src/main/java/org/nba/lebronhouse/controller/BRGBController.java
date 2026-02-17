package org.nba.lebronhouse.controller;

import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.dto.requests.SetBrgbColorRequest;
import org.nba.lebronhouse.service.BRGBService;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/api/brgb")
@RequiredArgsConstructor
public class BRGBController {

    private final BRGBService brgbService;

    @PutMapping()
    public ResponseEntity<Void> setBRGBColor(@RequestBody SetBrgbColorRequest request) {
        brgbService.setBRGBColor(request);
        return ResponseEntity.ok().build();
    }
}
