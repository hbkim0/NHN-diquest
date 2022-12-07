package com.diquest.infochatter3.restapi.model.workpedia;

import com.diquest.infochatter3.restapi.model.ChatRequest;
import lombok.*;

@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class WorkpediaChatRequest extends ChatRequest {
    private String userName;
    private QuizInfo quizInfo;

    @Getter
    @Setter
    @ToString
    @NoArgsConstructor
    @AllArgsConstructor
    public static class QuizInfo {
        private String dataType;
        private String setNo;
        private String no;
        private String answer;
    }
}
