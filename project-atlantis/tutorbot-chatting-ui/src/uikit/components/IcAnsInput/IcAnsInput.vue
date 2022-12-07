<!-- 입력 컴포넌트 -->
<template>
	<fieldset v-if="attribute.type == 'textarea'">
		<legend>{{ attribute.legend }}</legend>
		<div class="form_set">
			<div class="fs_bold">{{ attribute.legend }}</div>
			<textarea
				class="chat_form_gray"
				:placeholder="attribute.placeholder"
				:id="attribute.id"
				v-model="value"
				type="text"
				:readonly="this.readonly"
				:disabled="this.disabled"
				:class="this.class ? this.class : ''"
				:min="attribute.min"
				:max="attribute.max"
				:maxlength="attribute.length"
				rows="5"
				cols="20"
			></textarea
			><!-- 폭 지정할 경우 .cols 추가 후 cols값 입력 -->
		</div>
	</fieldset>

	<li v-else-if="attribute.type !== 'date'" :class="this.liClass">
		<label
			v-if="attribute.label"
			:for="attribute.id"
			:class="attribute.labelClass ? attribute.labelClass : 'type_text'"
			>{{ attribute.label }}
			<template v-if="attribute.btn">
				<div class="number_wrap">
					<button
						type="button"
						class="fas fa-minus-circle btn_qty qty_m"
						:disabled="this.disabled"
						@click="onClickMinus"
					/>
					<input
						:id="attribute.id"
						v-model="value"
						type="text"
						:readonly="this.readonly"
						:disabled="this.disabled"
						:class="
							this.class ? this.class : 'chat_form_white w-100px align_center'
						"
						:min="attribute.min"
						:max="attribute.max"
						:maxlength="attribute.length"
					/>
					<button
						type="button"
						class="fas fa-plus-circle btn_qty qty_p"
						:disabled="this.disabled"
						@click="onClickPlus"
					/>
				</div>
			</template>
			<template v-else>
				<input
					:id="attribute.id"
					v-model="value"
					:type="attribute.type"
					:class="this.class ? this.class : 'chat_form_white'"
					:readonly="this.readonly"
					:disabled="this.disabled"
					:min="attribute.min"
					:max="attribute.max"
					:placeholder="attribute.placeholder"
					:maxlength="attribute.length"
				/>
			</template>
		</label>

		<template v-else-if="attribute.btn">
			<div class="number_wrap">
				<button
					type="button"
					class="fas fa-minus-circle btn_qty qty_m"
					:disabled="this.disabled"
					@click="onClickMinus"
				/>
				<input
					:id="attribute.id"
					v-model="value"
					type="text"
					:readonly="this.readonly"
					:disabled="this.disabled"
					:class="
						this.class ? this.class : 'chat_form_white w-100px align_center'
					"
					:min="attribute.min"
					:max="attribute.max"
					:maxlength="attribute.length"
				/>
				<button
					type="button"
					class="fas fa-plus-circle btn_qty qty_p"
					:disabled="this.disabled"
					@click="onClickPlus"
				/>
			</div>
		</template>
		<template v-else>
			<input
				:id="attribute.id"
				v-model="value"
				:type="attribute.type"
				:class="this.class ? this.class : 'chat_form_white'"
				:readonly="this.readonly"
				:disabled="this.disabled"
				:min="attribute.min"
				:max="attribute.max"
				:placeholder="attribute.placeholder"
				:maxlength="attribute.length"
			/>
		</template>
	</li>
	<li v-else-if="attribute.type == 'date'" class="form_set type_datepicker">
		<!-- datepicker 일경우 li 에 .type_datepicker 추가 -->
		<!--
      configs: {
        enableTime: false,
        dateFormat: "Y-m-d",
        locale: "ko",
        disableMobile: "true",
      },			
		-->
		<div :class="dateClass" class="mt-5px">
			<flat-pickr
				v-if="this.configs.use"
				:id="'datepicker' + idx"
				ref="datePicker"
				v-model="value"
				:placeholder="attribute.placeholder"
				:class="
					this.class
						? this.class
						: 'basicDate chat_form_gray w-230px chat_form_white'
				"
				:readonly="this.readonly"
				:disabled="this.disabled"
				:config="this.configs"
				:events="['onDayCreate']"
				@on-day-create="onDayCreate"
			/>
			<a class="input-button" title="달력 보기/닫기" data-toggle></a>
		</div>
	</li>
</template>
<script>
import flatPickr from 'vue-flatpickr-component';
// theme is optional
// try more themes at - https://chmln.github.io/flatpickr/themes/
import '../../assets/css/flatpickr.css';
import 'flatpickr/dist/l10n/ko.js';
// eslint-disable-next-line no-unused-vars
export default {
	name: 'IcAnsInput',
	components: {
		'flat-pickr': flatPickr,
	},
	props: {
		idx: Number, // 메시지 번호
		nodeId: String, // 노드 식별자
		autoClick: Boolean, // input 에 버튼이 없을경우
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
					liClass: {
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
					type: {
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
					btn: {
						// 숫자 버튼형 (추가)
						type: String,
						default: null,
					},
					min: {
						// 숫자 최소값 (추가)
						type: String,
						default: null,
					},
					max: {
						// 숫자 최대값 (추가)
						type: String,
						default: null,
					},
					config: {
						// 날짜 속성 (추가)
						type: Object,
						default: null,
					},
					transferLabel: {
						// 엔진
						type: String,
						default: null,
					},
					displayLabel: {
						//  보여지는
						type: String,
						default: null,
					},
					transferText: {
						type: String,
						default: null,
					},
					displayText: {
						type: String,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			value: '',
			events: [],
			configs: {
				enableTime: false,
				dateFormat: 'Y-m-d',
				locale: 'ko',
				disableMobile: 'true',
			},
			dateClass: '',
		};
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
		readonly: function() {
			if (this.attribute) {
				if (this.attribute.readonly) {
					return String(this.attribute.readonly).toLowerCase() === 'true'
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
						if (row == 'icInputClass1') {
							classArray.push('chat_form_gray');
						} else if (row == 'icInputClass2') {
							classArray.push('chat_form_gray w-100px align_center');
						} else if (row == 'icInputClass3') {
							classArray.push('w-230px chat_form_white');
							this.dateClass = 'basicDate';
						} else if (row == 'icInputClass4') {
							classArray.push('w-230px chat_form_white');
							this.dateClass = 'basicDate_full';
						} else if (row == 'icInputClass5') {
							classArray.push('w-230px chat_form_white');
							this.dateClass = 'rangeDate';
						} else if (row == 'icInputClass6') {
							classArray.push('w-230px chat_form_white');
							this.dateClass = 'rangeDate_full';
						} else {
							classArray.push(row);
						}
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
		liClass: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.liClass) {
					// class
					this.attribute.liClass.split(' ').forEach(row => {
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
	watch: {
		// 컨포넌트간 데이터 공유
		value: function(value) {
			let transferText = value;
			let displayText = value;
			let dqml = '';
			if (this.attribute['transfer-text']) {
				transferText = this.attribute['transfer-text'];
				transferText = transferText
					.replace(/&amp;/g, '&')
					.replace(/&lt;/g, '<')
					.replace(/&gt;/g, '>')
					.replace(/&num;/g, '#');
			}

			if (this.attribute['display-text']) {
				displayText = this.attribute['display-text'];
				displayText = displayText
					.replace(/&amp;/g, '&')
					.replace(/&lt;/g, '<')
					.replace(/&gt;/g, '>')
					.replace(/&num;/g, '#');
			}
			
			// &lt; 문자를 < 특수문자로 치환
			if(this.attribute['value']) {
			  this.attribute['value']
			    .replace(/&amp;/g, '&')
				.replace(/&lt;/g, '<')
				.replace(/&gt;/g, '>')
				.replace(/&num;/g, '#');
			}
			if(this.attribute['placeholder']) {
			  this.attribute['placeholder']
			    .replace(/&amp;/g, '&')
				.replace(/&lt;/g, '<')
				.replace(/&gt;/g, '>')
				.replace(/&num;/g, '#');
			}
			if(this.attribute['text']) {
			  this.attribute['text']
			    .replace(/&amp;/g, '&')
				.replace(/&lt;/g, '<')
				.replace(/&gt;/g, '>')
				.replace(/&num;/g, '#');
			}

			if (this.attribute['dqml']) {
				dqml = this.attribute['dqml'];
			}

			if (this.autoClick) {
				if (transferText.replace(/ /gi, '')) {
					this.eventBus.$emit('ic-component-input-data', {
						idx: this.idx,
						nodeId: this.nodeId,
						transferText: transferText,
						displayText: displayText,
						dqml: dqml,
						action: this.autoClick ? 'qry' : 'none',
						probSet: {prob_num: this.attribute.label, answer: transferText.split(',').map(v => v.trim())},
					});
				}
			} else {
				this.eventBus.$emit('ic-component-input-data', {
					idx: this.idx,
					nodeId: this.nodeId,
					transferText: transferText,
					displayText: displayText,
					dqml: dqml,
					action: this.autoClick ? 'qry' : 'none',
					probSet: {prob_num: this.attribute.label, answer: transferText.split(',').map(v => v.trim())},
				});
			}
		},
	},

	created() {
		this.eventBus.$on('ic-input-scroll', data => {
			console.log(data);
			if (this.$refs.datePicker && this.$refs.datePicker.fp) {
				this.$refs.datePicker.fp.close();
			}
		});
		if (this.attribute) {
			let event = {};
			if (this.attribute.event) {
				event = JSON.parse(this.attribute.event);
			}

			if (this.attribute.config) {
				if (this.attribute.config == 'basic') {
					this.configs = {
						enableTime: false,
						dateFormat: 'Y-m-d',
						locale: 'ko',
						disableMobile: 'true',
						static: false,
						wrap: true,
					};
				}
				if (this.attribute.config == 'popup') {
					this.configs = {
						enableTime: false,
						dateFormat: 'Y-m-d',
						locale: 'ko',
						animate: false,
						disableMobile: 'true',
						wrap: true,
						onOpen: [
							function() {
								var element = document.getElementsByClassName(
									'flatpickr-calendar',
								);
								for (let i = 0; i < element.length; i++) {
									element[i].className += ' fullsize';
								}
							},
						],
						onClose: [
							function() {
								var element = document.getElementsByClassName(
									'flatpickr-calendar',
								);
								for (let i = 0; i < element.length; i++) {
									element[i].classList.remove('fullsize');
								}
							},
						],
					};
				}
				if (this.attribute.config == 'basicRange') {
					this.configs = {
						mode: 'range',
						locale: 'ko',
						disableMobile: 'true',
						dateFormat: 'Y-m-d',
						static: false,
						wrap: true,
					};
				}
				if (this.attribute.config == 'popupRange') {
					this.configs = {
						mode: 'range',
						animate: false,
						locale: 'ko',
						dateFormat: 'Y-m-d',
						disableMobile: 'true',
						wrap: true,
						onOpen: [
							function() {
								var element = document.getElementsByClassName(
									'flatpickr-calendar',
								);
								for (let i = 0; i < element.length; i++) {
									element[i].className += ' fullsize';
								}
							},
						],
						onClose: [
							function() {
								var element = document.getElementsByClassName(
									'flatpickr-calendar',
								);
								for (let i = 0; i < element.length; i++) {
									element[i].classList.remove('fullsize');
								}
							},
						],
					};
				}

				console.log(event);
				console.log(this.configs);

				if (event.minDate) {
					this.configs.minDate = event.minDate;
				}

				if (event.maxDate) {
					this.configs.maxDate = event.maxDate;
				}

				if (event.date) {
					this.events = event.date;
				}

				if (event.enable) {
					this.configs.enable = event.enable;
				}

				this.configs.use = true;
			} else {
				this.configs = {
					enableTime: false,
					dateFormat: 'Y-m-d',
					locale: 'ko',
					disableMobile: 'true',
				};

				this.configs.use = true;
			}

			if (this.attribute.text) {
				this.value = this.attribute.text;
			} else {
				this.value = ' ';
				setTimeout(() => {
					this.value = '';
				}, 1);
			}
		}
	},
	methods: {
		getFormatDate(date) {
			var year = date.getFullYear();
			var month = 1 + date.getMonth();
			month = month >= 10 ? month : '0' + month;
			var day = date.getDate();
			day = day >= 10 ? day : '0' + day;
			return year + '-' + month + '-' + day;
		},
		onDayCreate(dObj, dStr, fp, dayElem) {
			if (this.events) {
				this.events.forEach(event => {
					if (event.date == this.getFormatDate(dayElem.dateObj)) {
						let style = '';
						if (event.color) {
							style = 'color:' + event.color;
						}
						dayElem.innerHTML +=
							"<span class='event' style=" +
							style +
							'>' +
							event.text +
							'</span>';
					}
				});
			}
		},
		onClickMinus() {
			if (this.value > this.attribute.min) {
				this.value--;
			} else {
				alert('값이 ' + this.attribute.min + '보다 커야 합니다.');
			}
		},
		onClickPlus() {
			if (this.value < this.attribute.max) {
				this.value++;
			} else {
				alert('값이 ' + this.attribute.max + '보다 작아야 합니다.');
			}
		},
	},
};
</script>
<style>
.flatpickr-day .event {
	position: absolute;
	border-radius: 150px;
	content: ' ';
	display: block;
	font-size: 8px;
	height: 8px;
	line-height: 8px;
	width: 100%;
	left: 0px;
	text-align: center;
	bottom: 2px;
	letter-spacing: -1px;
}

.flatpickr-day {
	border-radius: 5px !important;
}

.flatpickr-day.selected.startRange,
.flatpickr-day.startRange.startRange,
.flatpickr-day.endRange.startRange {
	border-radius: 5px 0 0 5px !important;
}

.flatpickr-day.selected.endRange,
.flatpickr-day.startRange.endRange,
.flatpickr-day.endRange.endRange {
	border-radius: 0 5px 5px 0 !important;
}
</style>
