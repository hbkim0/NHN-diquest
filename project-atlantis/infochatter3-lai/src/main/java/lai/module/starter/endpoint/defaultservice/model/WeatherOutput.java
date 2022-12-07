package lai.module.starter.endpoint.defaultservice.model;

import com.diquest.lai.module.Param;

public class WeatherOutput {

  @Param(description = "지역", required = true, sample = "서울")
  private String city;

  @Param(description = "날짜", required = true, sample = "2020-02-17 00:00:00")
  private String date;

  @Param(description = "기온", required = true, sample = "0")
  private String temp;

  @Param(description = "체감온도", required = true, sample = "0")
  private String feelTemp;

  @Param(description = "날씨", required = true, sample = "Clear")
  private String weath;

  @Param(description = "풍속", required = true, sample = "0")
  private String wind;

  public String getCity() {
    return city;
  }

  public void setCity(String city) {
    this.city = city;
  }

  public String getDate() {
    return date;
  }

  public void setDate(String date) {
    this.date = date;
  }

  public String getTemp() {
    return temp;
  }

  public void setTemp(String temp) {
    this.temp = temp;
  }

  public String getWeath() {
    return weath;
  }

  public void setWeath(String weath) {
    this.weath = weath;
  }

  public String getFeelTemp() {
    return feelTemp;
  }

  public void setFeelTemp(String feelTemp) {
    this.feelTemp = feelTemp;
  }

  public String getWind() {
    return wind;
  }

  public void setWind(String wind) {
    this.wind = wind;
  }

}
