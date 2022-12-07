package lai.module.starter.endpoint.defaultservice.model;

import java.util.List;
import com.diquest.lai.module.Param;

public class NewsOutput {

  @Param(description = "뉴스 리스트", required = true, sample = "뉴스 리스트")
  private List<News> newsList;

  @Param(description = "조회 일시", required = true, sample = "2020.09.22 09:00")
  private String searchDt;

  public List<News> getNewsList() {
    return newsList;
  }

  public void setNewsList(List<News> newsList) {
    this.newsList = newsList;
  }

  public String getSearchDt() {
    return searchDt;
  }

  public void setSearchDt(String searchDt) {
    this.searchDt = searchDt;
  }

  public static class News {
    public News() {
      title = "";
      newsLink = "";
    }

    @Param(description = "제목", required = true, sample = "뉴스 제목")
    private String title;

    @Param(description = "접속 URL", required = true, sample = "http://news.naver.com")
    private String newsLink;

    public String getTitle() {
      return title;
    }

    public void setTitle(String title) {
      this.title = title;
    }

    public String getNewsLink() {
      return newsLink;
    }

    public void setNewsLink(String newsLink) {
      this.newsLink = newsLink;
    }
  }

}


