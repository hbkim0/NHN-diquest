<!-- 셀렉트박스 컴포넌트 -->
<template>
	<li>
		<label v-if="attribute.label" :for="attribute.id" class="type_text"
			>{{ attribute.label }} </label
		><select
			v-model="value"
			:class="this.class"
			:disabled="this.disabled"
			:id="attribute.id ? attribute.id : null"
		>
			<option disabled value="">선택</option>
			<option
				v-for="(row, index) in attribute.item"
				:key="row.id"
				:value="index"
				>{{ row.displayText }}</option
			>
		</select>
	</li>
</template>
<script>
export default {
	name: 'ic-ans-select',
	props: {
		idx: Number, // 메시지 번호
		nodeId: String, // 노드 식별자
		isDisabled: Boolean,
		/**
		 * attribute
		 * XSD 적용 완료-20200311
		 */
		attribute: {
			id: {
				// element에 id를 부여하여 구분할 때 사용
				type: String,
				default: null,
			},
			class: {
				// css와 같이 element에 공통으로 style을 적용할 때 사용
				type: String,
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
				// element가 표시될 때 텍스트
				type: String,
				default: null,
			},
			displayText: {
				// 버튼 클릭시 챗봇 표시 발화 default는 text value
				type: String,
				default: null,
			},
			item: {
				// Select 목록 (item{option, value})
				type: Array,
				default: null,
			},
			disabled: {
				// 해당항목 비활성화
				type: String,
				default: null,
			},
		},
	},
	data() {
		return {
			value: '',
		};
	},
	watch: {
		// 컨포넌트간 데이터 공유
		value: function(value) {
			let transferText = null;
			let dqml = null;
			let transferText_item = this.attribute.item[value].transferText;
			let displayText = this.attribute.item[value].displayText;
			let dqml_item = this.attribute.item[value].dqml;
			if (displayText) {
				if (this.attribute['transfer-text']) {
					transferText = this.attribute['transfer-text'];
				}
				if (this.attribute['display-text']) {
					displayText = this.attribute['display-text'];
				}
			} else {
				transferText = '';
				displayText = '';
			}

			if (this.attribute['dqml']) {
				dqml = this.attribute['dqml'];
			}

			if (dqml) {
				if (dqml_item && transferText_item) {
					transferText_item = dqml_item + ':' + transferText_item;
				}
			}

			if (
				this.attribute.item[value].disableYn &&
				this.attribute.item[value].disableId &&
				this.attribute.item[value].disableYn.toLowerCase() === 'y'
			) {
				this.eventBus.$emit('ic-component-button-disabled', {
					id: this.attribute.item[value].disableId,
					flag: 'Y',
				});
			} else if (
				this.attribute.item[value].disableYn &&
				this.attribute.item[value].disableId
			) {
				this.eventBus.$emit('ic-component-button-disabled', {
					id: '',
					flag: 'N',
				});
			}

			this.eventBus.$emit('ic-component-select-data', {
				idx: this.idx,
				nodeId: this.nodeId,
				transferText: transferText,
				displayText: displayText,
				transferText_item: transferText_item,
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
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						if (row == 'icSelectClass1') {
							classArray.push('chat_form_gray');
						} else {
							classArray.push(row);
						}
					});
				} else {
					classArray.push('chat_form_white');
				}

				// 속성에 있는 추가 스타일
				/*				
				if (this.attribute.align) {
					// align
					if (this.attribute.align == 'vertical') {
						// code
					} else if (this.attribute.align == 'horizontal') {
						// code
						classArray.push('horizontal');
					}
				}
				*/
			}

			return classArray.toString().replace(/,/g, ' ');
		},
	},
	mounted() {},
};
</script>
<style></style>
