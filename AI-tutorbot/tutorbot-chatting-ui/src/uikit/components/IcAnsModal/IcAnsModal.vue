<!-- 모달 컴포넌트 -->
<template>
	<!-- 내용 start -->
	<div class="chat_modal_cont overflow_auto">
		<slot></slot>
	</div>
	<!--// 내용 end -->
</template>
<script>
export default {
	name: 'ic-ans-modal',
	props: {
		items: {
			type: Array,
			default: null,
		},
		/**
		 * attribute
		 * XSD 적용 완료-20200311
		 */
		attribute: {
			type: Object,
			default: function() {
				return {
					id: {
						// layout 식별하기 위한 id
						type: String,
						default: null,
					},
					class: {
						// css와 같이 element에 공통으로 style을 적용할 때 사용
						type: Object,
						default: null,
					},
					emotion: {
						// default align은 세로방향 emotion 없으면  default 아이콘… : 사용자정의
						type: String,
						default: null,
					},
					type: {
						// type 없으면 기본 팝업 slide : 슬라이딩팝업… : 사용자정의
						type: String,
						default: null,
					},
					align: {
						// 하위 레이아웃 및 컴포넌트 배열 방향
						type: String,
						default: null,
					},
					scroll: {
						// 스크롤 여부
						type: String,
						default: null,
					},
				};
			},
		},
	},
	mounted() {},
};
</script>
<style></style>
