package com.ex.kafka.controller;

import com.ex.kafka.model.User;
import com.ex.kafka.producer.UserKafkaSender;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserKafkaSender userKafkaSender;

    @PostMapping
    public String sendData(@RequestBody User user) {
        return userKafkaSender.send(user);
    }
}
