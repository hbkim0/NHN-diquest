package lai.module.starter.endpoint.example.model;

import com.diquest.lai.module.Param;

public class Hello {

    @Param(description = "이름", required = true, sample = "홍길동")
    private String name;

    @Param(description = "인사말", required = true, sample = "안녕하세요! 홍길동님")
    private String message;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

}
