package com.diquest.infochatter3.restapi.config;

import java.util.ArrayList;
import java.util.List;
import org.springframework.context.EnvironmentAware;
import org.springframework.context.annotation.Bean;
import org.springframework.core.env.Environment;
import com.diquest.infochatter2.iuml.IumlParser;
import com.diquest.infochatter2.iuml.layout.DefaultLayout;
import com.diquest.infochatter2.iuml.layout.Layout;
import com.diquest.infochatter2.iuml.view.AnchorView;
import com.diquest.infochatter2.iuml.view.ButtonView;
import com.diquest.infochatter2.iuml.view.ImageView;
import com.diquest.infochatter2.iuml.view.InputView;
import com.diquest.infochatter2.iuml.view.TextView;
import com.diquest.infochatter2.iuml.view.View;
import com.diquest.infochatter3.client.Infochatter3Client;
import com.diquest.infochatter3.client.Infochatter3Config;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;

/**
 * 인포채터 설정
 */
@Slf4j
public class InfochatterConfig implements EnvironmentAware {

  @Setter
  private Environment environment;

  /**
   * IUML 파서 설정
   *
   * <pre>
   * 인포채터 답변은 IUML 문법으로 작성된다.
   * UI 표현할 수 있도록 IUML 파서가 필요하며
   * 파서에서 사용할 Layout 과 View 설정한다.
   * </pre>
   */
  @Bean
  public IumlParser iumlParser() {
    IumlParser parser = new IumlParser();
    // DefaultLayout
    // 대응되는 Layout 없는 경우 사용되면 기본값
    parser.setDefaultLayout(new DefaultLayout());

    // Layout 목록
    List<Layout> layouts = new ArrayList<>();
    layouts.add(new DefaultLayout());
    parser.setLayouts(layouts);

    // View 목록
    List<View> views = new ArrayList<>();
    views.add(new AnchorView());
    views.add(new ButtonView());
    views.add(new ImageView());
    views.add(new TextView());
    views.add(new InputView());
    parser.setViews(views);

    return parser;
  }

  /**
   * 인포채터3 클라이언트 설정
   *
   * <pre>
   * RESTAPI 사용할 인포채터3 클라이언트를 생성하며
   * 접속정보는 설정파일에서 설정가능하다.
   * </pre>
   */
  @Bean
  public Infochatter3Client infochatter3Client() {
    Infochatter3Config config = new Infochatter3Config();
    config.setIp(environment.getProperty("app.engine.host"));
    config.setPort(environment.getProperty("app.engine.port", Integer.class));
    config.setTimeout(environment.getProperty("app.engine.timeout", Integer.class));
    config.setMaxPoolSize(environment.getProperty("app.engine.maxPoolSize", Integer.class));
    config.setMinPoolSize(environment.getProperty("app.engine.minPoolSize", Integer.class));

    log.info("Client created. ({}:{})", config.getIp(), config.getPort());

    return new Infochatter3Client(config);
  }

}
