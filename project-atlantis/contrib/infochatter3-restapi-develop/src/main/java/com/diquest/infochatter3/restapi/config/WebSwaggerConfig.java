package com.diquest.infochatter3.restapi.config;

import java.util.ArrayList;
import java.util.Arrays;
import javax.servlet.http.HttpServletResponse;
import lombok.Setter;
import org.springframework.context.EnvironmentAware;
import org.springframework.context.annotation.Bean;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.RequestMethod;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.builders.ResponseMessageBuilder;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.VendorExtension;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@EnableSwagger2
public class WebSwaggerConfig implements EnvironmentAware {

  @Setter
  private Environment environment;

  @Bean
  public Docket docket() {
    // API 정보
    ApiInfo apiInfo = new ApiInfo(
        environment.getProperty("app.name"),
        environment.getProperty("app.description"),
        environment.getProperty("app.version"),
        null, null, null, null,
        new ArrayList<VendorExtension>()
    );

    return new Docket(DocumentationType.SWAGGER_2)
        .apiInfo(apiInfo)
        .useDefaultResponseMessages(false)
        .globalResponseMessage(RequestMethod.POST, Arrays.asList(
            // 401
            new ResponseMessageBuilder()
                .code(HttpServletResponse.SC_UNAUTHORIZED)
                .message("Unauthorized")
                .build()
            // 403
            , new ResponseMessageBuilder()
                .code(HttpServletResponse.SC_FORBIDDEN)
                .message("Forbidden")
                .build()
            // 404
            , new ResponseMessageBuilder()
                .code(HttpServletResponse.SC_NOT_FOUND)
                .message("Not Found")
                .build()
            // 500
            , new ResponseMessageBuilder()
                .code(HttpServletResponse.SC_INTERNAL_SERVER_ERROR)
                .message("Internal Server Error")
                .build()
            // 503
            , new ResponseMessageBuilder()
                .code(HttpServletResponse.SC_SERVICE_UNAVAILABLE)
                .message("Service Unavailable")
                .build()
            )
        )
        .select()
        .apis(RequestHandlerSelectors.any())
        .build();
  }

}
