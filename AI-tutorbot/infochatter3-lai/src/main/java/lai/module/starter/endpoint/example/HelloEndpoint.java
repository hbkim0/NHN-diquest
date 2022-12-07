package lai.module.starter.endpoint.example;

import com.diquest.lai.module.Endpoint;
import com.diquest.lai.module.EndpointMapping;
import lai.module.starter.endpoint.example.model.GoodbyeInput;
import lai.module.starter.endpoint.example.model.GoodbyeOutput;
import lai.module.starter.endpoint.example.model.Hello;

/**
 * Endpoint Class
 * <p>
 * Endpoint Class 는 여러개의 Endpoint 로 구성된다. '@Endpoint'은 Endpoint Class 임을 명시한다.
 * <p>
 * 예) ConceptEndpoint 의 정보 Endpoint Class: ConceptEndpoint Endpoint Method: hello, goodbye Endpoint:
 * concept.hello, concept.goodbye Key: concept.hello.output, concept.goodbye.output
 */
@Endpoint
public class HelloEndpoint {

  /**
   * Endpoint
   * <p>
   * Endpoint 는 Endpoint Method 와 Endpoint Mapping 으로 구성된다.
   * <p>
   * - Endpoint Mapping '@EndpointMapping'는 Method 가 Endpoint Method 임을 명시한다. ModuleName,
   * EndpointMapping.value 로 고유 Endpoint Key 를 생성한다. EndpintMapping.value 값이 없으면 MethodName 을 사용한다.
   * <p>
   * - Endpoint Method: 구현부
   */
  @EndpointMapping(mapping = "인사말", description = "인사말 앤드포인트")
  public Hello hello(Hello input) {
    String name = input.getName();
    String message = name + "님 안녕하세요!";

    Hello output = new Hello();
    output.setName(name);
    output.setMessage(message);

    return output;
  }

  @EndpointMapping(mapping = "맺음말", description = "맺음말 앤드포인트")
  public GoodbyeOutput goodbye(GoodbyeInput input) {
    String name = input.getInput();
    String message = name + "님 다음에 또 만나요~";

    GoodbyeOutput output = new GoodbyeOutput();
    output.setOutput(message);

    return output;
  }

}
