package org.nba.lebronhouse.controller;


import lombok.RequiredArgsConstructor;
import org.nba.lebronhouse.state.HouseState;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/api/person-count")
@RequiredArgsConstructor
public class PersonCountController {

    private final HouseState houseState;

    @PutMapping("/reset")
    public ResponseEntity<Void> resetPersonCount() {
        houseState.resetPersonCount();
        return ResponseEntity.ok().build();
    }

    @GetMapping()
    public ResponseEntity<Integer> getPersonCount() {
        return ResponseEntity.ok(
                houseState.getPersonInside()
        );
    }
}
