package lai.module.starter.endpoint.timeedu.model;

import com.diquest.lai.module.Param;

public class HomeworkOutput {
	
	@Param(description = "학생 이름", required = true, sample = "김지수")
	private String userName;
	
	@Param(description = "교재명", required = true, sample = "팩토연산C03")
	private String bookTitle;

	@Param(description = "오늘 맞춘 문항수", required = true, sample = "12")
	private String correctCount;
	
	@Param(description = "전체 맞춘 문항수", required = true, sample = "489")
	private String correctCountAll;

	@Param(description = "정답률", required = true, sample = "90")
	private int correctRate;
	
	@Param(description = "전체 푼 쪽수", required = true, sample = "68")
	private String pageDone;
	
	@Param(description = "교재 남은 쪽수", required = true, sample = "52")
	private String pageRemained;
	
	@Param(description = "오늘 숙제 쪽수", required = true, sample = "66, 68")
	private String pagesToday;
	
	@Param(description = "오늘 숙제 쪽수 카운트", required = true, sample = "2")
	private String pagesTodayCount;

	@Param(description = "내일 숙제 쪽수", required = true, sample = "72, 73")
	private String pagesTomorrow;
	
	@Param(description = "학습자 유형", required = true, sample = "열공형")
	private String personType;
	
	public void setUserName(String userName) {
		this.userName = userName;
	}

	public void setBookTitle(String bookTitle) {
		this.bookTitle = bookTitle;
	}

	public void setCorrectCount(String correctCount) {
		this.correctCount = correctCount;
	}
	
	public void setCorrectCountAll(String correctCountAll) {
		this.correctCountAll = correctCountAll;
	}
	
	public void setCorrectRate(int correctRate) {
		this.correctRate = correctRate;
	}

	public void setPageDone(String pageDone) {
		this.pageDone = pageDone;
	}
	
	public void setPageRemained(String pageRemained) {
		this.pageRemained = pageRemained;
	}
	
	public void setPagesToday(String pagesToday) {
		this.pagesToday = pagesToday;
	}
	
	public void setPagesTodayCount(String pagesTodayCount) {
		this.pagesTodayCount = pagesTodayCount;
	}

	public void setPagesTomorrow(String pagesTomorrow) {
		this.pagesTomorrow = pagesTomorrow;
	}

	public void setPersonType(String personType) {
		this.personType = personType;
	}

}
