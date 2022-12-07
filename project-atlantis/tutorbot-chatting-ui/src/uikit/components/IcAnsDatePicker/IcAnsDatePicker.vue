<!-- 데이터피커 컴포넌트 -->
<template>
	<li class="type_datepicker">
		<!-- datepicker 일경우 li 에 .type_datepicker 추가 -->
		<flat-pickr
			:placeholder="attribute.placeholder"
			:class="this.class"
			:id="attribute.id"
			:disabled="this.disabled"
			:config="attribute.config"
		>
		</flat-pickr
		><label
			:for="attribute.id"
			class="far fa-calendar-alt text_large"
			:title="attribute.title"
		></label>
	</li>
</template>
<script>
// import this component
import flatPickr from 'vue-flatpickr-component';
// theme is optional
// try more themes at - https://chmln.github.io/flatpickr/themes/
import 'flatpickr/dist/l10n/ko.js';

export default {
	name: 'ic-ans-date',
	components: {
		'flat-pickr': flatPickr,
	},
	props: {
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
						type: String,
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
					types: {
						type: String,
						default: null,
					},
					placeholder: {
						// 답변 발화 표시후 자동 실행 element가 있는 경우 (예, 선택 팝업)
						type: String,
						default: null,
					},
					text: {
						// 인풋창 기본값
						type: String,
						default: null,
					},
					length: {
						// 입력길이 제한
						type: String,
						default: null,
					},
					readonly: {
						// 읽기전용
						type: String,
						default: null,
					},
					disabled: {
						// 해당항목 비활성화
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
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						classArray.push(row);
					});
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
