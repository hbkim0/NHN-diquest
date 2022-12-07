<!-- 말풍선 컴포넌트 -->
<template>
	<hr v-if="this.class == 'hrTag'" />
	<div v-else-if="!delay" :class="this.class" :style="bubbleStyle">
		<slot></slot>
	</div>
	<div v-else>
		<div class="bot_text">
			<div class="chat_loading">
				<span class="bg_clip">답변 준비중</span>
			</div>
		</div>
	</div>
</template>
<script>
export default {
	name: 'ic-ans-bubble',
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
					style: {
						// 스타일 캐로셀
						type: String,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			delay: false,
			closeItem: null,
			bubbleStyle: '',
		};
	},
	computed: {
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						if (row == 'icBubbleClass1') {
							classArray.push('bot_text');
						} else if (row == 'icBubbleClass2') {
							classArray.push('out_cont');
						} else if (row == 'icBubbleClass3') {
							classArray.push('bot_card medium');
						} else if (row == 'icBubbleClass4') {
							classArray.push('bot_card small');
						} else if (row == 'icBubbleClass5') {
							classArray.push('bot_card large');
						} else if (row == 'icBubbleClass6') {
							classArray.push('bot_card large item');
						} else if (row == 'icBubbleClass7') {
							classArray.push('bot_cont_item type_inline');
						} else if (row == 'icBubbleClass8') {
							classArray.push('bot_text full');
						} else if (row == 'icBubbleClass9') {
							classArray.push('bot_card medium item');
						} else if (row == 'icBubbleClass10') {
							classArray.push('item bot_card_text');
						} else if (row == 'icBubbleClass11') {
							// 2컬럼 버튼 시 .full 추가
							classArray.push('bot_text full');
						} else if (row == 'icBubbleClass12') {
							// 오류메시지
							classArray.push('bot_text error');
						} else if (row == 'icBubbleClass13') {
							// 답변준비중
							classArray.push('chat_loading');
						} else if (row == 'icBubbleClass14') {
							// 답변준비중
							classArray.push('bot_card full');
						} else {
							classArray.push(row);
						}
					});
				} else {
					classArray.push('bot_cont_item');
					classArray.push('bot_text');
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
		this.eventBus.$on('ic-component-button-close', data => {
			this.componentButtonClose(data);
		});
	},
	mounted() {
		this.bubbleStyle = this.attribute.style;
		if (this.attribute.delay) {
			this.delay = true;
			setTimeout(() => (this.delay = false), Number(this.attribute.delay));
		} else {
			this.delay = false;
		}
	},
	methods: {
		componentButtonClose(data) {
			this.closeItem = data.id;
			if (this.attribute.id === data.id) {
				this.bubbleStyle += ';display:none;';
			}
		},
	},
};
</script>
<style>
.removeItem {
	display: none;
}
</style>
