package com.ex.kafka.consumer;

import com.ex.kafka.model.User;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.common.KafkaException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class UserKafkaConsumer {

    @Value("${app.kafka.topic}")
    private String topicName;

    @Autowired
    @Qualifier("userKafkaProducerTemplate")
    private KafkaTemplate<String, User> userKafkaTemplate;

    @KafkaListener(topics = "${app.kafka.topic}", groupId = "${app.kafka.consumer-group-id}", containerFactory = "concurrentKafkaListenerUserConsumerFactory")
    @Retryable(value = KafkaException.class, maxAttempts = 3, backoff = @Backoff(delay = 3000))
    public void receive(User user) {
        log.info("received data='{}={}' from {}", user.hashCode(), user, topicName);
    }
}
