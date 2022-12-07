package lai.module.starter.sample;

import com.diquest.lai.*;
import com.diquest.lai.client.LaiClient;
import com.diquest.lai.client.LaiClientConfig;
import com.diquest.lai.logger.LoggerWrapper;
import com.diquest.lai.logger.LoggerWrapperFactory;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

import java.util.*;

public class TimeEndpointTests {

    private static final LoggerWrapper log =
            LoggerWrapperFactory.createLogger(TimeEndpointTests.class);

    private static LaiClient client;

    @BeforeClass
    public static void init() {
        LaiClientConfig config = new LaiClientConfig();
//        config.setBaseUrl("http://ic3dev.bot.diquest.com//lai2");
        config.setBaseUrl("http://localhost:8085/lai");
        config.setIgnoreCertificateError(false);
        client = new LaiClient();
        client.setConfig(config);
    }

//    @Test
    public void getModuleList() {
        SpecResult specresult = client.spec().queryAll();
        if (specresult != null) {
            List<SpecModule> modules = specresult.getModules();
            for (SpecModule item : modules) {
                String moduleName = item.getModuleInfo().getName();
                System.out.println("moduleName : " + moduleName);
//                System.out.println(item);
//                for (SpecEndpoint endpoint : item.getEndpoints()) {
//                    System.out.println("\tendpoint : " + endpoint);
//                }
            }
        }
    }

  @Test
        public void hello() {
            Map<String, String> param = new HashMap<>();
            param.put("name", "홍길동");

            LookupValue value1 = client.lookup().query("Example.인사말.message", param);
            log.info(">> {}", value1);
            Assert.assertEquals("홍길동님 안녕하세요!", value1.getValue());

            String value2 = client.lookup().queryValue("Example.인사말.message", param, String.class);
            log.info(">> {}", value2);
            Assert.assertEquals("홍길동님 안녕하세요!", value2);
        }

    @Test
    public void getNews() {
        Map<String, String> param = new HashMap<>();

        LookupValue value1 = client.lookup().query("DEFAULT-Service.뉴스조회.newsList", param);
        List<Map> newsList = (List)value1.getValue();
        for(Map n : newsList){
            log.info(">> {}", n);
        }
//        Assert.assertEquals("홍길동님 안녕하세요!", value1.getValue());

    }

//  @Test
        public void currentTime() {
            List<String> keys = new ArrayList<>();
            keys.add("시작.시간.현재.date");
            keys.add("시작.시간.현재.time");
            keys.add("시작.시간.현재.datetime");

            LookupResult result = client.lookup().query(keys);
            log.info("Date: {}", result.getValue("시작.시간.현재.date"));
            log.info("Time: {}", result.getValue("시작.시간.현재.time"));
            log.info("Datetime: {}", result.getValue("시작.시간.현재.datetime"));
        }

//  @Test
        public void weather() {
            Map<String, String> param = new HashMap<>();
            param.put("city", "1835848");

            LookupValue value1 = client.lookup().query("시작.날씨.message", param);
            log.info(">> {}", value1);
            Assert.assertEquals("서울 날씨 조회", value1.getValue());

            String value2 = client.lookup().queryValue("시작.날씨.message", param, String.class);
            log.info(">> {}", value2);
            Assert.assertEquals("서울 날씨 조회2", value2);
        }
    }
