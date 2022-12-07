package lai.module.starter.config;

import com.diquest.lai.ModuleInfo;
import com.diquest.lai.module.servlet.ModuleConfigure;
import lai.module.starter.endpoint.defaultservice.ExchangeEndpoint;
import lai.module.starter.endpoint.example.HelloEndpoint;
import lai.module.starter.endpoint.defaultservice.NewsEndpoint;
import lai.module.starter.endpoint.example.TimeEndpoint;
import lai.module.starter.endpoint.timeedu.ExplanationEndpoint;
import lai.module.starter.endpoint.timeedu.HomeworkEndpoint;
import lai.module.starter.endpoint.timeedu.ScoringEndpoint;
import lai.module.starter.endpoint.defaultservice.WeatherEndpoint;

/**
 * LAI Module 설정
 * <p>
 * LAI Module 은 자바설정을 사용합니다. 설정객체는 ModuleConfigurer 객체를 상속받습니다.
 */
public class ModuleConfig extends ModuleConfigure {

  public ModuleConfig() {
      ModuleInfo m = new ModuleInfo();
      m.setName("DEFAULT");
      m.setVersion("1.0.0-SNAPSHOT");
      m.setDescription("LAI START_MODULE PROJECT");
      setModule(m);
      setEndpoint(m.getName(), new WeatherEndpoint());
      setEndpoint(m.getName(), new NewsEndpoint());
      setEndpoint(m.getName(), new ExchangeEndpoint());

      ModuleInfo m2 = new ModuleInfo();
      m2.setName("Example");
      m2.setVersion("1.0.0-SNAPSHOT");
      m2.setDescription("LAI START_MODULE PROJECT");
      setModule(m2);
      setEndpoint(m2.getName(), new HelloEndpoint());
      setEndpoint(m2.getName(), new TimeEndpoint());
      
      ModuleInfo m3 = new ModuleInfo();
      m3.setName("Tutorbot");
      m3.setVersion("1.0.0-SNAPSHOT");
      m3.setDescription("LAI START_MODULE PROJECT");
      setModule(m3);
      setEndpoint(m3.getName(), new ExplanationEndpoint());
      setEndpoint(m3.getName(), new HomeworkEndpoint());
      setEndpoint(m3.getName(), new ScoringEndpoint());
  }
}
