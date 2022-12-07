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
import lai.module.starter.endpoint.defaultservice.model.NewsInput;
import lai.module.starter.endpoint.defaultservice.model.NewsOutput;

@Endpoint
public class NewsEndpoint {

  @EndpointMapping(mapping = "뉴스조회", description = "뉴스조회 앤드포인트")
  public NewsOutput searchNews(NewsInput input) {
    NewsOutput newsOutput = new NewsOutput();

    BufferedInputStream bis = null;
    BufferedReader reader = null;
    HttpURLConnection conn = null;

    Date date = new Date();
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy년 MM월 dd일 HH:mm");

    newsOutput.setSearchDt(sdf.format(date));

    // HttpsURLConnection conn = null;

    String newsUrl = "https://news.naver.com";
    List<NewsOutput.News> list = new LinkedList<NewsOutput.News>();
    try {
      URL url = new URL(newsUrl);
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
      reader = new BufferedReader(new InputStreamReader(bis, "EUC-KR"));
      StringBuffer st = new StringBuffer();
      String line;
      while ((line = reader.readLine()) != null) {
        st.append(line + "\n");
      }

      Document doc = Jsoup.parse(st.toString());
      Elements root = doc.select("div.hdline_article_tit a");


      for (Element el : root) {
        NewsOutput.News news = new NewsOutput.News();

        news.setTitle(el.text());
        news.setNewsLink(newsUrl + el.attr("href"));

        list.add(news);

      }
      newsOutput.setNewsList(list);

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
    return newsOutput;

  }

}
