package lai.module.starter.endpoint.example.model;

import com.diquest.lai.module.Param;

public class GoodbyeInput {

    @Param(description = "이름", required = true, sample = "홍길동")
    private String input;

    public String getInput() {
        return input;
    }

    public void setInput(String input) {
        this.input = input;
    }

}
