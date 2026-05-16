package com.ex.kafka.producer;

import com.ex.kafka.model.User;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.common.KafkaException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Recover;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Component;

import java.util.UUID;

@Component
@Slf4j
public class UserKafkaSender {

    @Autowired
    @Qualifier("userKafkaProducerTemplate")
    private KafkaTemplate<String, User> userKafkaTemplate;

    @Value("${app.kafka.topic:test_topic}")
    private String topicName;

    @Value("${app.kafka.enabled:false}")
    private boolean isKafkaEnabled;


    @Retryable(value = KafkaException.class, maxAttempts = 3, backoff = @Backoff(delay = 3000))
    public String send(User user) {
        log.info("sending data='{}={}' to topic='{}'", user.hashCode(), user, topicName);
        String key = UUID.randomUUID().toString();
        if (isKafkaEnabled) {
            userKafkaTemplate.send(topicName, key, user);
            return "data sent successfully";
        }
        return "kafka is disabled in application";
    }

    @Recover
    public void recoverKafkaMessage(KafkaException exception) {
        log.error("sending data to error queue with message: {}", exception.getMessage());
    }
}
