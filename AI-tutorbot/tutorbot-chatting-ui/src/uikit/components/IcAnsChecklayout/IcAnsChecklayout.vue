<!-- 체크박스 레이아웃 컴포넌트 -->
<template>
	<fieldset v-if="attribute.fieldSet">
		<legend>상품선택</legend>
		<ul :class="this.class" :style="attribute.style">
			<slot></slot>
		</ul>
	</fieldset>
	<ul v-else :class="this.class" :style="attribute.style">
		<slot></slot>
	</ul>
</template>
<script>
export default {
	name: 'ic-ans-checklayout',
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
					classArray.push('form_set');
				}

				// 속성에 있는 추가 스타일
				if (this.attribute.align) {
					// align
					if (this.attribute.align == 'vertical') {
						// code
					} else if (this.attribute.align == 'horizontal') {
						// code
						classArray.push('horizontal');
					}
				}
				if (this.attribute.scroll) {
					// scroll
					if (
						this.attribute.scroll == 'wrap' ||
						this.attribute.scroll == 'off'
					) {
						// code
					} else if (this.attribute.scroll == 'on') {
						// code
					}
				}
			}

			return classArray.toString().replace(/,/g, ' ');
		},
	},
	mounted() {},
};
</script>
<style></style>
