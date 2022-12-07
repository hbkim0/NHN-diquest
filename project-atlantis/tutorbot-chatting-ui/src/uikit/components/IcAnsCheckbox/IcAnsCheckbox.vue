<!-- 체크박스 컴포넌트 -->
<template>
	<label :for="idx + '_' + nodeId">
		<input
			:disabled="this.disabled"
			v-model="value"
			type="checkbox"
			:id="idx + '_' + nodeId"
		/>{{ attribute.text }}</label
	>
</template>
<script>
export default {
	name: 'ic-ans-checkbox',
	props: {
		idx: Number, // 메시지 번호
		nodeId: String, // 노드 식별자
		isDisabled: Boolean,
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
					auto: {
						// 답변 발화 표시후 자동 실행 element가 있는 경우 (예, 선택 팝업)
						type: String,
						default: null,
					},
					text: {
						// Element가 표시될 때 text
						type: Array,
						default: null,
					},
					transferText: {
						// Element가 클릭될 때 챗봇에 전달되는 발화
						type: String,
						default: null,
					},
					displayText: {
						// 버튼 클릭시 챗봇 표시 발화 default는 text value
						type: String,
						default: null,
					},
					disabled: {
						// 해당항목 비활성화
						type: String,
						default: null,
					},
					checked: {
						// 해당항목 체크활성화
						type: String,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			value: false,
		};
	},
	watch: {
		// 컨포넌트간 데이터 공유
		value: function(value) {
			let transferText = '';
			let displayText = '';
			let dqml = '';
			if (value) {
				if (this.attribute['transfer-text']) {
					transferText = this.attribute['transfer-text'];
					transferText = transferText
						.replace(/&amp;/g, '&')
						.replace(/&lt;/g, '<')
						.replace(/&gt;/g, '>')
						.replace(/&num;/g, '#');
				} else {
					transferText = this.attribute.text;
				}
				if (this.attribute['display-text']) {
					displayText = this.attribute['display-text'];
					displayText = displayText
						.replace(/&amp;/g, '&')
						.replace(/&lt;/g, '<')
						.replace(/&gt;/g, '>')
						.replace(/&num;/g, '#');
				} else {
					displayText = this.attribute.text;
				}
			} else {
				transferText = '';
				displayText = '';
			}

			if (this.attribute['dqml']) {
				dqml = this.attribute['dqml'];
			}

			this.eventBus.$emit('ic-component-checkbox-data', {
				idx: this.idx,
				nodeId: this.nodeId,
				transferText: transferText,
				displayText: displayText,
				dqml: dqml,
				action: 'none',
			});
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
	mounted() {
		if (this.attribute) {
			if (this.attribute.checked) {
				if (String(this.attribute.checked).toLowerCase() === 'true') {
					this.value = this.attribute.text;
				}
			}
		}
	},
};
</script>
<style></style>
