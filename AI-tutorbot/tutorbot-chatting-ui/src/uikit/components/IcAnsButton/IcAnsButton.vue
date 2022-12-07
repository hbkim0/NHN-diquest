<!-- 버튼 컴포넌트 -->
<template>
	<span
		v-if="attribute.type == 'text'"
		:class="this.class"
		:disabled="this.disabled"
		@click.prevent.stop="onClickButton"
		:style="attribute.style"
		ref="attribute.id2"
		>{{ attribute.label }}</span
	>
	<button
		v-else
		:class="this.class"
		:disabled="this.disabled || this.disableFlag"
		:style="attribute.style"
		@click.prevent.stop="onClickButton"
		ref="attribute.id2"
		:id="attribute.id ? attribute.id : null"
	>
		{{ attribute.label }}
		<template
			v-if="attribute.textAlign == 'right' || attribute.textAlign == 'bottom'"
		>
			<img v-if="attribute.imgSrc" v-lazy="imgObj" :title="attribute.title" />
			<i v-if="attribute.iClass" :class="attribute.iClass"></i>
			<span v-if="attribute.iLabel">{{ attribute.iLabel }}</span>
		</template>
		<template
			v-else-if="attribute.textAlign == 'left' || attribute.textAlign == 'top'"
		>
			<span v-if="attribute.iLabel">{{ attribute.iLabel }}</span>
			<i v-if="attribute.iClass" :class="attribute.iClass"></i>
			<img v-if="attribute.imgSrc" v-lazy="imgObj" :title="attribute.title" />
		</template>
		<template v-else>
			<i v-if="attribute.iClass" :class="attribute.iClass"></i>
		</template>
	</button>
</template>
<script>
export default {
	name: 'ic-ans-button',
	props: {
		idx: Number, // 메시지 번호
		nodeId: String, // 노드 식별자
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
						required: false,
					},
					label: {
						// 버튼에 표시할 텍스트
						type: Array,
						default: null,
					},
					transferText: {
						// 버튼 클릭시 챗봇 발화 default는 text value
						type: String,
						default: null,
					},
					displayText: {
						// 버튼 클릭시 챗봇 표시 발화 default는 text value
						type: String,
						default: null,
					},
					textAlign: {
						// 이미지버튼 인 경우 이미지를 기준으로 텍스트의 위치
						type: String,
						default: null,
					},
					src: {
						// 바로가기 링크 url
						type: String,
						default: null,
					},
					target: {
						// 바로가기 링크시 새창 옵션
						type: String,
						default: null,
					},
					disabled: {
						// 해당항목 비활성화
						type: Boolean,
						default: false,
					},
					imgSrc: {
						// 이미지 버튼인 경우 이미지 주소
						type: String,
						default: null,
					},
					iClass: {
						// 아이콘 클래스
						type: String,
						default: null,
					},
					iLabel: {
						// 아이콘 라벨
						type: String,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			imgObj: {
				src: this.attribute.imgSrc,
			},
			disableFlag: false,
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
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						if (row == 'icBtnClass1') {
							classArray.push('btn');
							classArray.push('medium lightbluegreen');
						} else if (row == 'icBtnClass2') {
							classArray.push('btn');
							classArray.push('medium lightbluegreen_bd');
						} else if (row == 'icBtnClass3') {
							classArray.push('btn');
							classArray.push('medium blue');
						} else if (row == 'icBtnClass4') {
							classArray.push('btn');
							classArray.push('medium blue_bd');
						} else if (row == 'icBtnClass5') {
							classArray.push('btn');
							classArray.push('medium gray');
						} else if (row == 'icBtnClass6') {
							classArray.push('btn');
							classArray.push('medium gray_bd');
						} else if (row == 'icBtnClass7') {
							classArray.push('btn');
							classArray.push('medium darkgray');
						} else if (row == 'icBtnClass8') {
							classArray.push('btn');
							classArray.push('medium darkgray_bd');
						} else if (row == 'icBtnClass9') {
							classArray.push('btn');
							classArray.push('small primary_c_bd');
						} else if (row == 'icBtnClass10') {
							classArray.push('btn');
							classArray.push('medium primary_c_bd');
						} else if (row == 'icBtnClass11') {
							classArray.push('btn');
							classArray.push('large primary_c_bd');
						} else if (row == 'icBtnClass12') {
							classArray.push('btn');
							classArray.push('small primary_c');
						} else if (row == 'icBtnClass13') {
							classArray.push('btn');
							classArray.push('medium primary_c');
						} else if (row == 'icBtnClass14') {
							classArray.push('btn');
							classArray.push('large primary_c');
						} else if (row == 'icBtnClass15') {
							classArray.push('type_icon_box');
						} else if (row == 'icBtnClass16') {
							classArray.push('btn_bot_modal');
						} else if (row == 'icBtnClass17') {
							classArray.push('');
						} else if (row == 'icBtnClass18') {
							classArray.push('btn small gray type_square');
						} else if (row == 'icBtnClass19') {
							classArray.push(
								'mr-5px w-30px align_right gray_hover fas fa-times text_large float_right',
							);
						} else {
							classArray.push(row);
						}
					});
				} else {
					classArray.push('btn');
					classArray.push('medium primary_c_bd');
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
	created() {
		this.eventBus.$on('ic-component-button-disabled', data => {
			this.componentButtonDisabled(data);
		});
	},
	mounted() {},
	methods: {
		onClickButton: function() {
			if (this.attribute.modal) {
				this.eventBus.$emit('ic-component-modal', {
					idx: this.idx,
					nodeId: this.nodeId,
					modalId: this.attribute.modal,
				});
				return;
			}

			if (this.attribute.src) {
				// code
				let target = '_blank';
				if (this.attribute.target) {
					target = this.attribute.target;
				}
				let find = /^tel:|^sms:|^mailto:/g;

				if (find.test(this.attribute.src)) {
					window.location.href = this.attribute.src;
				} else {
					window.open(this.attribute.src, target);
				}
			} else {
				if (this.attribute['transfer-text']) {
					const trasText = this.attribute['transfer-text'];
					this.attribute['transfer-text'] = trasText
						.replace(/&amp;/g, '&')
						.replace(/&lt;/g, '<')
						.replace(/&gt;/g, '>')
						.replace(/&num;/g, '#');
				}
				const params = {
					idx: this.idx,
					nodeId: this.nodeId,
					action: 'confirm',
					transferText: this.attribute['transfer-text']
						? this.attribute['transfer-text']
						: this.attribute.label,
					displayText: this.attribute['display-text']
						? this.attribute['display-text']
						: this.attribute.label,
				};

				if (this.attribute['transfer-text']) {
					params.transferText_real = this.attribute['transfer-text'];
				}
				if (this.attribute['data']) {
					params.data = this.attribute['data'];
				}
				if (this.attribute['dqml']) {
					params.dqml = this.attribute['dqml'];
				}
				if (this.attribute['chat-event-id']) {
					params.chat_event_id = this.attribute['chat-event-id'];
				}
				this.eventBus.$emit('ic-component-modal', {
					idx: this.idx,
					nodeId: this.nodeId,
					close: 'true',
				});

				if (this.attribute.id) {
					this.eventBus.$emit('ic-component-button-close', {
						id: this.attribute.id,
						idx: this.idx,
						nodeId: this.nodeId,
						modalId: this.attribute.modal,
					});
					params.dqml = 'removeItem';
				}
				this.eventBus.$emit('ic-component-button-click', params);
			}
		},
		componentButtonDisabled(data) {
			if (data.flag && data.flag === 'N') {
				this.disableFlag = false;
			} else {
				if (this.attribute.id === data.id) {
					this.disableFlag = true;
				}
			}
		},
	},
};
</script>
<style scoped>
span {
	cursor: pointer;
}
</style>
