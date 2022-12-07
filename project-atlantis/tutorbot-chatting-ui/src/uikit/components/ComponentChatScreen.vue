<template>
	<div class="chat_wrapper">
		<div class="chat_area chat_theme_basic">
			<div class="chat_user">
				<button
					type="button"
					class="btn_simul_sub fas fa-search-plus align-middle hover mr-5px"
					name="simul_info"
					title="분석보기"
				></button
				><!-- 분석보기 : 인포채터3 관리도구용 -->
				<div class="chat_text">
					ㅇㅇㅇ 에 관해 알려주세요.
				</div>
				<div class="chat_date right">오후 5:34</div>
			</div>

			<div class="chat_bot">
				<!-- 프로필 아이콘 start -->
				<div class="bot_profile"><span class="bg_clip">챗봇명</span></div>
				<!--// 프로필 아이콘 end -->

				<div class="bot_cont_wrap">
					<slot></slot>
					<!-- chat foot start -->
					<div class="chat_foot">
						<div class="chat_date left">오후 5:34</div>
					</div>
					<!--// chat foot end -->
				</div>
			</div>
		</div>
	</div>
</template>
<script>
export default {
	name: 'component-chat-screen',
	props: {
		com: {
			// element에 id를 부여하여 구분할 때 사용
			type: String,
			default: null,
		},
	},
	mounted() {},
};
</script>
<style></style>
