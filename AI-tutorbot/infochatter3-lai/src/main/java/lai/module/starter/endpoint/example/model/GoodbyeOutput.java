package lai.module.starter.endpoint.example.model;

import com.diquest.lai.module.Param;

public class GoodbyeOutput {

    @Param(description = "반환 메시지", required = true, sample = "홍길동님 안녕하세요!")
    private String output;

    public String getOutput() {
        return output;
    }

    public void setOutput(String output) {
        this.output = output;
    }

}
