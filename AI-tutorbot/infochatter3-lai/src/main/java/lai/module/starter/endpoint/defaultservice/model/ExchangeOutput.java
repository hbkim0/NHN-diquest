package lai.module.starter.endpoint.defaultservice.model;

import java.util.List;
import com.diquest.lai.module.Param;

public class ExchangeOutput {

  @Param(description = "환율 리스트", required = true, sample = "환율 리스트")
  private List<Exchange> exchangeList;

  @Param(description = "조회 일시", required = true, sample = "2020.09.22 09:00")
  private String searchDt;

  public List<Exchange> getExchangeList() {
    return exchangeList;
  }

  public void setExchangeList(List<Exchange> exchangeList) {
    this.exchangeList = exchangeList;
  }

  public String getSearchDt() {
    return searchDt;
  }

  public void setSearchDt(String searchDt) {
    this.searchDt = searchDt;
  }

  public static class Exchange {

    @Param(description = "국가", required = true, sample = "미국")
    private String country;

    @Param(description = "통화", required = true, sample = "달러")
    private String currency;

    @Param(description = "환율", required = true, sample = "1100")
    private String exchange;

    @Param(description = "환율 변동", required = true, sample = "-1.10")
    private String change;

    @Param(description = "접속 URL", required = true, sample = "https://finance.daum.net/exchanges")
    private String exchangeLink;


    public String getCountry() {
      return country;
    }

    public void setCountry(String country) {
      this.country = country;
    }

    public String getCurrency() {
      return currency;
    }

    public void setCurrency(String currency) {
      this.currency = currency;
    }

    public String getExchange() {
      return exchange;
    }

    public void setExchange(String exchange) {
      this.exchange = exchange;
    }

    public String getChange() {
      return change;
    }

    public void setChange(String change) {
      this.change = change;
    }

    public String getExchangeLink() {
      return exchangeLink;
    }

    public void setExchangeLink(String exchangeLink) {
      this.exchangeLink = exchangeLink;
    }

  }

}


