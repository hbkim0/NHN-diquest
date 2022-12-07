package com.diquest.infochatter3.restapi.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.MessageSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;
import org.springframework.context.support.MessageSourceAccessor;
import org.springframework.context.support.PropertySourcesPlaceholderConfigurer;
import org.springframework.context.support.ReloadableResourceBundleMessageSource;

@Slf4j
@ComponentScan("com.diquest.infochatter3")
@PropertySources({
    @PropertySource(value = "classpath:config/application.properties")
})
@Import({
    // Infochatter
    InfochatterConfig.class
    // Web - MVC
    , WebMvcConfig.class
    // Web - Swagger
    , WebSwaggerConfig.class
})
public class ApplicationConfig {

  @Bean
  public MessageSource messageSource() {
    ReloadableResourceBundleMessageSource messageSource = new ReloadableResourceBundleMessageSource();
    messageSource.setBasenames(
        "classpath:messages/error", "classpath:messages/message"
    );
    messageSource.setUseCodeAsDefaultMessage(true);
    messageSource.setFallbackToSystemLocale(false);
    messageSource.setDefaultEncoding("UTF-8");
    messageSource.setCacheSeconds(3600);

    return messageSource;
  }

  @Bean
  public MessageSourceAccessor messageSourceAccessor() {
    return new MessageSourceAccessor(messageSource());
  }

  /**
   * {@link org.springframework.beans.factory.annotation.Value} 를 사용하기 위해선
   * PropertySourcesPlaceholderConfigurer 를 Bean 으로 등록해야한다.
   *
   * @see <a href="http://kwonnam.pe.kr/wiki/springframework/propertysource">springframework:propertysource
   * [권남]</a>
   */
  @Bean
  public static PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
    return new PropertySourcesPlaceholderConfigurer();
  }

}
