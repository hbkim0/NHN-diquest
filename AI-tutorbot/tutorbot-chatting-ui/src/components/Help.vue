<template>
	<div class="chat_wrapper">
		<!--  모달 : 도움말 start -->
		<div
			id="modal_help"
			class="chat_modal type_carousel full2"
			style="display: block; position: fixed;"
		>
			<div class="chat_modal_in">
				<div class="chat_modal_head">
					<div class="primary_c">
						<strong>도움말</strong>
					</div>
					<button class="btn_modal_close fas fa-times" @click="close">
						<span class="bg_clip">닫기</span>
					</button>
				</div>

				<!-- 내용 start -->
				<div class="chat_modal_cont overflow_auto full">
					<!-- 도움말 캐로셀 (dot-auto) start -->

					<carousel
						:loop="false"
						:autoWidth="false"
						:autoHeight="false"
						:margin="3"
						:nav="false"
						:dots="true"
						:items="1"
						:smartSpeed="400"
					>
						<div class="item">
							<img
								src="../assets/img_chatbot/help/help_screen01.png"
								alt="도움말 화면 1"
							/>
						</div>
						<div class="item">
							<img
								src="../assets/img_chatbot/help/help_screen02.png"
								alt="도움말 화면 2"
							/>
						</div>
						<div class="item">
							<img
								src="../assets/img_chatbot/help/help_screen03.png"
								alt="도움말 화면 3"
							/>
						</div>
						<div class="item">
							<img
								src="../assets/img_chatbot/help/help_screen04.png"
								alt="도움말 화면 4"
							/>
						</div>
						<div class="item">
							<img
								src="../assets/img_chatbot/help/help_screen05.png"
								alt="도움말 화면 5"
							/>
						</div>
					</carousel>

					<!--// 도움말 캐로셀 (nav-auto) end -->
				</div>
				<!--// 내용 end -->
			</div>
		</div>
		<!--// 모달 : 도움말 end -->
	</div>
</template>

<script>
import carousel from 'vue-owl-carousel';

export default {
	name: 'Help',
	components: { carousel },
	methods: {
		close() {
			this.$emit('close');
		},
	},
};
</script>
<style scoped>
.owl-carousel {
	height: calc(100% - 50px);
}
.owl-stage-outer {
	height: 100%;
}
.owl-stage {
	height: 100%;
}
.owl-item {
	height: 100%;
}
.item {
	height: 100%;
}
.item img {
	max-height: 100%;
	max-width: 100%;
	margin: 0 auto;
	width: auto;
}
</style>
