package lai.module.starter.endpoint.example;

import java.util.Calendar;
import java.util.Date;
import com.diquest.lai.module.Endpoint;
import com.diquest.lai.module.EndpointMapping;
import lai.module.starter.endpoint.example.model.Time;
import lai.module.starter.endpoint.example.model.TimeInp;

@Endpoint
public class TimeEndpoint {

  @EndpointMapping(mapping = "시간.현재", description = "현재시간 정보")
  public Time currentTime(TimeInp time) {
    return new Time(new Date());
  }

  @EndpointMapping(mapping = "시간.하루전", description = "하루전 시간 정보")
  public Time yesterdayTime(TimeInp time) {
    Calendar calendar = Calendar.getInstance();
    calendar.add(Calendar.DATE, -1);

    return new Time(calendar.getTime());
  }

}
