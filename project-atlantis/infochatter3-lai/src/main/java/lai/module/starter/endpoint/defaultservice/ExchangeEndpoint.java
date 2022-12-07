package lai.module.starter.endpoint.defaultservice;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import com.diquest.lai.module.Endpoint;
import com.diquest.lai.module.EndpointMapping;
import lai.module.starter.endpoint.defaultservice.model.ExchangeInput;
import lai.module.starter.endpoint.defaultservice.model.ExchangeOutput;

@Endpoint
public class ExchangeEndpoint {

  @EndpointMapping(mapping = "환율조회", description = "뉴스조회 앤드포인트")
  public ExchangeOutput searchExchange(ExchangeInput input) {
    ExchangeOutput exchangeOutput = new ExchangeOutput();

    BufferedInputStream bis = null;
    BufferedReader reader = null;
    HttpURLConnection conn = null;

    Date date = new Date();
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy년 MM월 dd일 HH:mm");

    exchangeOutput.setSearchDt(sdf.format(date));

    // HttpsURLConnection conn = null;

    String exchangesUrl =
        "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%ED%99%98%EC%9C%A8";

    String searchUrl = "https://search.naver.com/search.naver";
    List<ExchangeOutput.Exchange> list = new LinkedList<ExchangeOutput.Exchange>();
    try {
      URL url = new URL(exchangesUrl);
      conn = (HttpURLConnection) url.openConnection();
      // conn = (HttpsURLConnection) url.openConnection();
      // conn.setRequestProperty("user-agent",
      // "Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) "
      // + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36");

      conn.setRequestProperty("Accept",
          "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8");

      // SSLContext context = SSLContext.getInstance("TLS");
      // context.init(null, null, null);
      // conn.setSSLSocketFactory(context.getSocketFactory());
      conn.connect();
      conn.setInstanceFollowRedirects(true);


      bis = new BufferedInputStream(conn.getInputStream());
      reader = new BufferedReader(new InputStreamReader(bis));
      // reader = new BufferedReader(new InputStreamReader(bis, "EUC-KR"));
      StringBuffer st = new StringBuffer();
      String line;
      while ((line = reader.readLine()) != null) {
        st.append(line + "\n");
      }

      Document doc = Jsoup.parse(st.toString());
      Elements root = doc.select("table.rate_table_info tbody tr");

      exchangeOutput.setSearchDt(doc.select("p.grp_info").text());


      for (Element el : root) {
        ExchangeOutput.Exchange exchange = new ExchangeOutput.Exchange();
        exchange.setCurrency(el.select("th span em").text());
        el.select("th span em").remove();
        exchange.setCountry(el.select("th span").text());
        exchange.setExchangeLink(searchUrl + el.select("a").attr("href"));
        Elements subNode = el.select("td");
        for (int i = 0; i < subNode.size(); i++) {
          Element subEl = subNode.get(i);
          if (subEl.hasClass("flu_nm")) {
            exchange.setChange(subEl.select("span").get(0).text() + " "
                + (subEl.select("span").get(1).text().equals("하락") ? "-" : "+")
                + subEl.select("em").text());
          } else if (subEl.hasClass("flu_pct")) {

          } else {
            exchange.setExchange(subEl.select("span").text());
          }
        }
        list.add(exchange);
      }

      exchangeOutput.setExchangeList(list);

    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      try {
        bis.close();
        reader.close();
        conn.disconnect();

      } catch (Exception e) {
        e.printStackTrace();
      }
    }
    return exchangeOutput;

  }

}
