<!-- root 정의 컴포넌트 -->
<template>
	<div class="bot_cont">
		<div :class="this.class">
			<!-- 버튼셋 start -->
			<!-- 채팅  -->
			<slot></slot>
			<!--// 버튼셋 end -->
		</div>
	</div>
</template>
<script>
export default {
	name: 'ic-ans-iuml',
	props: {
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
				};
			},
		},
	},
	computed: {
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						classArray.push(row);
					});
				} else {
					classArray.push('bot_cont_item');
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
