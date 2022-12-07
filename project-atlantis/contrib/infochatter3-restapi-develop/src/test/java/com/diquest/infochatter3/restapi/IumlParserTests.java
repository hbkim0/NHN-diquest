package com.diquest.infochatter3.restapi;

import com.diquest.infochatter2.iuml.IumlParser;
import com.diquest.infochatter2.iuml.layout.Layout;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.junit.BeforeClass;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestName;

import java.util.List;

@Slf4j
public class IumlParserTests {

    private static ObjectMapper mapper;

    private static IumlParser parser;

    @BeforeClass
    public static void setUp() {
        // JSON Mapper
        mapper = new ObjectMapper();
        mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
        mapper.configure(DeserializationFeature.FAIL_ON_IGNORED_PROPERTIES, false);

        // IUML Parser
        parser = IumlParser.builder().build();
    }

    @Rule
    public TestName name = new TestName();

    private void printResult(String iuml) throws Exception {
        String format = "\n"
                + "=======================\n"
                + "{}\n"
                + "=======================\n"
                + "{}\n"
                + "=======================\n"
                + "{}\n"
                + "=======================";

        List<Layout> ret = parser.parse(iuml);

        log.info(format, name.getMethodName(), iuml, mapper.writerWithDefaultPrettyPrinter().writeValueAsString(ret));
    }

    @Test
    public void 텍스트() throws Exception {
        String iuml = "3in2_2in1 > 가동 중 누수 > 에어컨 실내기 배수호수로 물이빠지나요?\n"
                + "■ 원인\n"
                + "- 배수호수 끝 부분이 위로 올라와 있거나 물에 잠겨 있는 경우 또는 끝 부분이 꺾여 있으면 역류 현상으로 물이 샐 수 있습니다.\n"
                + "■ 조치방법\n"
                + "- 에어컨 내부에서 생긴 물이 밖으로 잘 빠지도록 배수 호스가 꺾이지 않게 해주시기 바랍니다.";

        printResult(iuml);
    }

    @Test
    public void 텍스트_다중문단() throws Exception {
        String iuml = "[p]게임을 하실래요?[/p]\n" +
                "[p]\n" +
                "게임목록\n" +
                "[list id=items]\n" +
                "  [button value='GAME-369']3.6.9 게임[/button]\n" +
                "  [button value='GAME-BASEBALL']야구게임[/button]\n" +
                "[/list]\n" +
                "[/p]";

        printResult(iuml);
    }

    @Test
    public void 텍스트_2버튼() throws Exception {
        String iuml = "[p]\n"
                + "고객님 해당 업무는 아직 제가 배우는 중입니다. 상담을 위해 고객센터 상담원을 연결해 드릴까요?\n"
                + "연결을 원하지 않으실 경우, 다른 문의 사항을 챗봇에 물어봐 주세요.\n"
                + "[button id=button1]계속 대화하기[/button]\n"
                + "[button id=button2]상담원 연결[/button]\n"
                + "[/p]\n";

        printResult(iuml);
    }

    @Test
    public void 텍스트_버튼목록_링크() throws Exception {
        String iuml = "[p]\n" +
                "어떤 종류의 통장을 만들고 싶으세요?\n" +
                "[list id=items]\n" +
                "\t[button value='입출금']입출금이 자유로운 ‘입출금식’[/button]\n" +
                "\t[button value='적금식']목돈을 만드는 ‘적금식’[/button]\n" +
                "\t[button value='예금식' disabled]목돈을 굴리는 ‘예금식’[/button]\n" +
                "[/list]\n" +
                "[a id=link url=http://www.diquest.com title='링크로 이동합니다.']자세히 보기[/a]\n" +
                "[/p]\n";

        printResult(iuml);
    }

    @Test
    public void 텍스트_이미지목록() throws Exception {
        String iuml = "[p]\n" +
                "'고양이' 이미지를 검색했습니다.\n" +
                "[list id=items]\n" +
                "  [img title='졸림' url=http://t.est/1.jpg]졸려요...[/img]\n" +
                "  [img url=http://t.est/2.jpg]멍.....[/img]\n" +
                "  [img url=http://t.est/a.jpg]a.jpg 이미지[/img]\n" +
                "  [img url=http://t.est/123.jpg]123.jpg 이미지[/img]\n" +
                "[/list]\n" +
                "[/p]\n";

        printResult(iuml);
    }

}
