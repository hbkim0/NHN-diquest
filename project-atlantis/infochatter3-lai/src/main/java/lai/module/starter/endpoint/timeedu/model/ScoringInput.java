package lai.module.starter.endpoint.timeedu.model;

import com.diquest.lai.module.Param;

public class ScoringInput {
	
	public static class Image {
		@Param(description = "아이디", required = true, sample = "ai01")
		private String userId;


		@Param(description = "이미지 URL", required = true, sample="input_url_A03_96_lz44OhQ.jpg")
		private String imgUrl;
		
		public String getUserId() {
			return userId;
		}
		
		public void setUserId(String userId) {
			this.userId = userId;
		}
		
		public String getImgUrl() {
			return imgUrl;
		}
		
		public void setImgUrl(String imgUrl) {
			this.imgUrl = imgUrl;
		}
	}
	
	public static class Submit {
		@Param(description = "아이디", required = true, sample = "ai01")
		private String userId;

		@Param(description = "제출 결과", required = true, sample="")
		private String submit;
		
		public String getUserId() {
			return userId;
		}
		
		public void setUserId(String userId) {
			this.userId = userId;
		}
		
		public String getSubmit() {
			return submit;
		}
		
		public void setSubmit(String submit) {
			this.submit = submit;
		}
	}
}
