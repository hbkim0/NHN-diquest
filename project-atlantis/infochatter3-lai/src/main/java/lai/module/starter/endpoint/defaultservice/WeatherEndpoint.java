package lai.module.starter.endpoint.defaultservice;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import com.diquest.lai.module.Endpoint;
import com.diquest.lai.module.EndpointMapping;
import lai.module.starter.endpoint.defaultservice.model.WeatherInput;
import lai.module.starter.endpoint.defaultservice.model.WeatherOutput;

/**
 * Endpoint Class
 * <p>
 * Endpoint Class 는 여러개의 Endpoint 로 구성된다. '@Endpoint'은 Endpoint Class 임을 명시한다.
 * <p>
 * 예) ConceptEndpoint 의 정보 Endpoint Class: ConceptEndpoint Endpoint Method: hello, goodbye Endpoint:
 * concept.hello, concept.goodbye Key: concept.hello.output, concept.goodbye.output
 */
@Endpoint
public class WeatherEndpoint {

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

  @EndpointMapping(mapping = "날씨조회", description = "날씨조회 앤드포인트")
  public WeatherOutput weatherlist(WeatherInput input) {
    String city = input.getCity() == null ? "서울" : input.getCity();
    String orgCity = city == "" ? "서울" : city;
    String key = "f30532b024280f2fb5dccc412a936be6";

    WeatherOutput output = new WeatherOutput();

    output.setCity(orgCity);

    JSONObject jo = new JSONObject();
    JSONParser jp = new JSONParser();

    if (city == "" || city.indexOf("서울") > -1) {
      city = "1835848";
    } else if (city.indexOf("부산") > -1) {
      city = "1838722";
    } else if (city.indexOf("대구") > -1) {
      city = "1835327";
    } else if (city.indexOf("인천") > -1) {
      city = "1843564";
    } else if (city.indexOf("광주") > -1) {
      city = "1841808";
    } else if (city.indexOf("대전") > -1) {
      city = "1835224";
    } else if (city.indexOf("울산") > -1) {
      city = "1833742";
    } else if (city.indexOf("강원") > -1) {
      city = "1843125";
    } else if (city.indexOf("경기") > -1) {
      city = "1841610";
    } else if (city.indexOf("경남") > -1 || city.indexOf("경상남도") > -1) {
      city = "1902028";
    } else if (city.indexOf("경북") > -1 || city.indexOf("경상북도") > -1) {
      city = "1841597";
    } else if (city.indexOf("전남") > -1 || city.indexOf("전라남도") > -1) {
      city = "1845788";
    } else if (city.indexOf("전북") > -1 || city.indexOf("전라북도") > -1) {
      city = "1845789";
    } else if (city.indexOf("충남") > -1 || city.indexOf("충청남도") > -1) {
      city = "1845105";
    } else if (city.indexOf("충북") > -1 || city.indexOf("충청북도") > -1) {
      city = "1845106";
    } else if (city.indexOf("제주") > -1) {
      city = "1846266";
    } else if (city.indexOf("부천") > -1) {
      city = "1838716";
    } else if (city.indexOf("성남") > -1) {
      city = "1897000";
    } else if (city.indexOf("안산") > -1) {
      city = "1846918";
    } else if (city.indexOf("안양") > -1) {
      city = "1846898";
    } else if (city.indexOf("용인") > -1) {
      city = "1832427";
    } else if (city.indexOf("평택") > -1) {
      city = "1838343";
    } else if (city.indexOf("화성") > -1) {
      city = "1843847";
    } else if (city.indexOf("청주") > -1) {
      city = "1845604";
    } else if (city.indexOf("김해") > -1) {
      city = "1842943";
    } else if (city.indexOf("창원") > -1) {
      city = "1846326";
    } else if (city.indexOf("전주") > -1) {
      city = "1845457";
    } else {
      output.setDate("");
      output.setTemp("");
      output.setFeelTemp("");
      output.setWeath("해당 도시의 날씨정보가 제공되지 않습니다.");
      output.setWind("");
      return output;
    }

    BufferedReader in = null;
    try {
      URL obj = new URL("http://api.openweathermap.org/data/2.5/forecast?id=" + city
          + "&lang=kr&units=Metric&cnt=1&appid=" + key); // 호출할
      HttpURLConnection con = (HttpURLConnection) obj.openConnection();
      con.setRequestMethod("GET");
      in = new BufferedReader(new InputStreamReader(con.getInputStream(), "UTF-8"));

      jo = (JSONObject) jp.parse(in);

      JSONArray ja = (JSONArray) jo.get("list");
      JSONObject tempJo = (JSONObject) ja.get(0);
      JSONObject mainJo = (JSONObject) tempJo.get("main");

      output.setDate(tempJo.get("dt_txt").toString());
      output.setTemp(mainJo.get("temp").toString());
      output.setFeelTemp(mainJo.get("feels_like").toString());
      ja = (JSONArray) tempJo.get("weather");
      mainJo = (JSONObject) ja.get(0);
      output.setWeath(mainJo.get("description").toString());
      mainJo = (JSONObject) tempJo.get("wind");
      output.setWind(mainJo.get("speed").toString());

    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      if (in != null)
        try {
          in.close();
        } catch (Exception e) {
          e.printStackTrace();
        }
    }
    return output;
  }
}
