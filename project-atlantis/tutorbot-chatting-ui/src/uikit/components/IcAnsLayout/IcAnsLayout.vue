<!-- 레이아웃 컴포넌트 -->
<template>
	<ic-ans-carousel
		v-if="this.attribute.scroll == 'on'"
		:attribute="this.attribute"
		><slot></slot
	></ic-ans-carousel>
	<ul v-else-if="type === 'list'" :class="this.class" :style="attribute.style">
		<slot></slot>
	</ul>
	<div v-else :class="this.class" :style="attribute.style">
		<slot></slot>
		<!--
		<li v-for="(item, i) in items" :key="i">
			<slot :name="item.slotName"></slot>
		</li>
		--></div>
</template>
<script>
import IcAnsCarousel from '../IcAnsCarousel';

export default {
	name: 'ic-ans-layout',
	components: {
		'ic-ans-carousel': IcAnsCarousel,
	},
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
					nav: {
						// 스크롤 여부
						type: Boolean,
						default: false,
					},
					dots: {
						// 스크롤 여부
						type: Boolean,
						default: false,
					},
					style: {
						// 스타일
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
						if (row == 'icLayoutClass1') {
							classArray.push('bot_btnset');
						} else if (row == 'icLayoutClass2') {
							classArray.push('bot_btnset full');
						} else if (row == 'icLayoutClass3') {
							classArray.push('bot_btnset type_check');
						} else if (row == 'icLayoutClass4') {
							classArray.push('bot_btnset type_radio');
						} else if (row == 'icLayoutClass5') {
							// 버튼셋 start : 2컬럼 버튼 시 .half 추가
							classArray.push('bot_btnset half');
						} else if (row == 'icLayoutClass6') {
							classArray.push('form_set');
						} else if (row == 'icLayoutClass7') {
							classArray.push('bot_listset');
							this.type = 'list';
						} else if (row == 'icLayoutClass8') {
							classArray.push('bot_listset overflow_auto');
							this.type = 'list';
						} else if (row == 'icLayoutClass9') {
							classArray.push('bot_btnset horizontal_full');
						} else if (row == 'icLayoutClass10') {
							classArray.push('list_dot text_medium_small mt-10px');
							this.type = 'list';
						} else if (row == 'icLayoutClass11') {
							classArray.push('list_dot');
							this.type = 'list';
						} else if (row == 'icLayoutClass12') {
							classArray.push('list_dot text_medium_small');
							this.type = 'list';
						} else if (row == 'icLayoutClass13') {
							classArray.push('list_dot mt-5px');
							this.type = 'list';
						} else if (row == 'icLayoutClass14') {
							classArray.push('');
						} else {
							classArray.push(row);
							if (row.indexOf('list_dot') != -1) {
								this.type = 'list';
							}
						}
					});
				} else {
					classArray.push('bot_btnset');
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
	data() {
		return {
			type: '',
		};
	},
	created() {},
};
</script>
<style></style>
