<!-- 링크 컴포넌트 -->
<template>
	<iframe
		width="100%"
		:height="attribute.height"
		:src="attribute.src"
		frameborder="0"
		style="border:0;"
		allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
		allowfullscreen
	></iframe>
</template>
<script>
export default {
	name: 'ic-ans-link',
	props: {
		items: {
			type: Array,
			default: null,
		},
		isDisabled: Boolean,
		/**
		 * attribute
		 * XSD 적용 완료-20200311
		 */
		attribute: {
			type: Object,
			default: function() {
				return {
					id: {
						// element에 id를 부여하여 구분할 때 사용
						type: String,
						default: null,
					},
					class: {
						// css와 같이 element에 공통으로 style을 적용할 때 사용
						type: Object,
						default: null,
					},
					data: {
						// Element에 데이터를 주고 받을 때 Json 포맷 대응
						type: String,
						default: null,
					},
					autoAction: {
						// 답변 발화 표시후 자동 실행 element가 있는 경우 (예, 선택 팝업)
						type: String,
						default: null,
					},
					text: {
						// Element가 표시될 때 text
						type: Array,
						default: null,
					},
					displayText: {
						// 버튼 클릭시 챗봇 표시 발화 default는 text value
						type: String,
						default: null,
					},
				};
			},
		},
	},
	computed: {
		disabled: function() {
			if (this.isDisabled) {
				return true;
			}
			if (this.attribute) {
				if (this.attribute.disabled) {
					return String(this.attribute.disabled).toLowerCase() === 'true'
						? true
						: false;
				}
			}
			return false;
		},
	},
	mounted() {},
};
</script>
<style></style>
