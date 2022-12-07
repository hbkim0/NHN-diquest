package lai.module.starter.endpoint.timeedu.model;

import com.diquest.lai.module.Param;

public class ExplanationInput {
	
	@Param(description = "교재명", required = true, sample = "소마셈 C5")
	private String bookTitle;
	
	@Param(description = "쪽수", required = true, sample = "66")
	private String page;
	
	@Param(description = "문제번호", required = true, sample = "1")
	private String problem;
	
	public String getBookTitle() {
		return bookTitle;
	}

	public String getPage() {
		return page;
	}
	
	public String getProblem() {
		return problem;
	}
}
