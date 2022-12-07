package lai.module.starter.endpoint.defaultservice.model;

import com.diquest.lai.module.Param;

public class WeatherInput {

  @Param(description = "지역", required = true, sample = "서울")
  private String city;

  public String getCity() {
    return city;
  }

  public void setCity(String city) {
    this.city = city;
  }
}
