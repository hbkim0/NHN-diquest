package com.diquest.infochatter3.restapi.config;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.http.MediaType;
import org.springframework.http.converter.ByteArrayHttpMessageConverter;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.ResourceHttpMessageConverter;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.servlet.config.annotation.*;
import org.springframework.web.servlet.mvc.WebContentInterceptor;

@EnableWebMvc
public class WebMvcConfig extends WebMvcConfigurerAdapter {

  @Autowired
  private ApplicationContext applicationContext;

  @Override
  public void configurePathMatch(PathMatchConfigurer configurer) {
    // 접미어 패턴매칭 OFF
    configurer.setUseSuffixPatternMatch(false);
  }

  @Override
  public void addResourceHandlers(ResourceHandlerRegistry registry) {
    registry.addResourceHandler("/**")
        .addResourceLocations("classpath:/META-INF/resources/", "classpath:/public/",
            "classpath:/resources/", "classpath:/static/");
  }

  @Override
  public void addInterceptors(InterceptorRegistry registry) {

  }

  @Override
  public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
    configurer
        .favorPathExtension(false)
        .ignoreAcceptHeader(false)
        .favorParameter(true)
        .useJaf(false)
        .parameterName("_format")
        .defaultContentType(MediaType.APPLICATION_JSON)
        .mediaType("json", MediaType.APPLICATION_JSON);
  }

  @Override
  public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
    // Byte[]
    converters.add(new ByteArrayHttpMessageConverter());
    // String
    StringHttpMessageConverter stringConverter = new StringHttpMessageConverter();
    stringConverter.setWriteAcceptCharset(false);
    converters.add(stringConverter);
    // application/octet-stream -> Resource 변환
    converters.add(new ResourceHttpMessageConverter());
    // JSON
    MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter =
        new MappingJackson2HttpMessageConverter(
            Jackson2ObjectMapperBuilder.json()
                .applicationContext(applicationContext)
                .serializationInclusion(JsonInclude.Include.NON_NULL)
                .build()
        );
    converters.add(mappingJackson2HttpMessageConverter);
  }

  /**
   * 캐시 비활성화 인터셉터 API 는 캐시가 필요 없음으로 비활성화
   */
  @Bean
  public WebContentInterceptor disableCacheInterceptor() {
    WebContentInterceptor interceptor = new WebContentInterceptor();
    interceptor.setCacheSeconds(0);
    interceptor.setUseExpiresHeader(true);
    interceptor.setUseCacheControlHeader(true);
    interceptor.setUseCacheControlNoStore(true);

    return interceptor;
  }

  @Override
  public void addCorsMappings(final CorsRegistry registry) {
    registry.addMapping("/**");
  }

}
