package lai.module.starter.endpoint.timeedu.model;

import java.util.List;
import com.diquest.lai.module.Param;

public class ScoringOutput {
	
	public static class RecognitionOutput {
		
		@Param(description = "응답 성공", required = true)
		private int success;
		
		@Param(description = "로그 ID", sample = "로그 ID")
		private String logId;
		
		@Param(description = "교재 이름", sample = "교재 이름")
		private String workbookName;
		
		@Param(description = "페이지 ID", sample = "페이지 ID")
		private String pageId;
		
		@Param(description = "페이지 번호", sample = "페이지 번호")
		private String pageNum;
		
		@Param(description = "영역 검출 이미지", sample = "영역 검출 이미지")
		private String boxedUrl;
		
		@Param(description = "추론 리스트", sample = "추론 리스트")
		private List<Recognition> recognitionList;
		
		public void setSuccess(int success) {
			this.success = success;
		}
		
		public void setLogId(String logId) {
			this.logId = logId;
		}
		
		public void setWorkbookName(String workbookName) {
			this.workbookName = workbookName;
		}
		
		public void setPageId(String pageId) {
			this.pageId = pageId;
		}
		
		public void setPageNum(String pageNum) {
			this.pageNum = pageNum;
		}
		
		public void setBoxedUrl(String boxedUrl) {
			this.boxedUrl = boxedUrl;
		}
		
		public void setRecognitionList(List<Recognition> recognitionList) {
			this.recognitionList = recognitionList;
		}
	}
	
	public static class ResultOutput {
		
		@Param(description = "응답 성공", required = true)
		private int success;
		
		@Param(description = "오답 유무", sample = "오답 유무")
		private int hasWrong;
		
		@Param(description = "오답 문제들", sample = "오답 문제들")
		private String wrongAnswer;
		
		public void setSuccess(int success) {
			this.success = success;
		}
		
		public int getHasWrong() {
			return hasWrong;
		}
		
		public void setHasWrong(int hasWrong) {
			this.hasWrong = hasWrong;
		}
		
		public String getWrongAnswer() {
			return wrongAnswer;
		}
		
		public void setWrongAnswer(String wrongAnswer) {
			this.wrongAnswer = wrongAnswer;
		}
	}

	public static class Recognition {
	    @Param(description = "문제번호", required = true, sample = "1")
		private String probNum;

	    @Param(description = "인식", required = true, sample = "10")
	    private String prediction;
 
	    public String getProbNum() {
	    	return probNum;
	    }
	       
	    public void setProbNum(String probNum) {
	    	this.probNum = probNum;
	    }
	    
	    public String getPrediction() {
	    	return prediction;
	    }
	    
	    public void setPrediction(String prediction) {
	    	this.prediction = prediction;
	    }
	    
	    public Recognition(String probNum, String prediction) {
	    	this.probNum = probNum;
	    	this.prediction = prediction;
	    }
	}
}
