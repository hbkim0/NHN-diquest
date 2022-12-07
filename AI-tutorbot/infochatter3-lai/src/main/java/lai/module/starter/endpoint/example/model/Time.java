package lai.module.starter.endpoint.example.model;

import java.text.SimpleDateFormat;
import java.util.Date;
import com.diquest.lai.module.Param;

public class Time {

  @Param(description = "일자", required = true, sample = "2017-01-01")
  private String date;

  @Param(description = "시간", required = true, sample = "15:00:00")
  private String time;

  @Param(description = "일자시간", required = true, sample = "2017-01-01 15:00:00")
  private String datetime;

  public Time() {}

  public Time(Date date) {
    SimpleDateFormat yyyyMMdd = new SimpleDateFormat("yyyy-MM-dd");

    SimpleDateFormat hhmmss = new SimpleDateFormat("hh:mm:ss");

    SimpleDateFormat yyyyMMddhhmmss = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
    this.date = yyyyMMdd.format(date);
    this.time = hhmmss.format(date);
    this.datetime = yyyyMMddhhmmss.format(date);
  }

  public String getDate() {
    return date;
  }

  public void setDate(String date) {
    this.date = date;
  }

  public String getTime() {
    return time;
  }

  public void setTime(String time) {
    this.time = time;
  }

  public String getDatetime() {
    return datetime;
  }

  public void setDatetime(String datetime) {
    this.datetime = datetime;
  }

}
