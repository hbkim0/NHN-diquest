<!-- 리스트 컴포넌트 -->
<template>
	<li v-if="this.btn" class="type_btn">
		<ul :class="this.class ? this.class : 'bot_btnset w-100p align_center'">
			<li>
				<button class="btn small gray">{{ attribute.text }}</button>
			</li>
		</ul>
	</li>
	<li
		v-else
		:style="
			attribute['list_id'] && pageShowNum && attribute['list_id'] > pageShowNum
				? 'display:none'
				: ''
		"
	>
		<slot v-if="attribute.align == 'left'" :attribute="attribute.image"></slot>
		<div :class="this.class ? this.class : 'bot_list_text'">
			<div class="text_strong">{{ attribute.title }}</div>
			<template v-for="(txt, index) in contText">
				{{ txt }} <br v-if="index < contText.length - 1" :key="txt.id" />
			</template>
		</div>
		<slot v-if="attribute.align == 'right'" :attribute="attribute.image"></slot>
	</li>
</template>
<script>
export default {
	name: 'ic-ans-layout-list',
	props: {
		idx: Number, // 메시지 번호
		nodeId: String, // 노드 식별자
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
					title: {
						// 제목
						type: String,
						default: null,
					},
					cont: {
						// 내용
						type: String,
						default: null,
					},
					btn: {
						// 버튼 여부
						type: String,
						default: null,
					},
					text: {
						// 버튼텍스트
						type: String,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			pageCount: 0,
			pageCurrent: 1,
			pageShowNum: null,
			changedItems: [],
			carouselItems: [],
			carouselAttribute: {
				style: '',
				autoWidth: false,
				nav: false,
				dots: true,
			},
		};
	},
	created() {
		this.eventBus.$on('ic-page-more', data => {
			this.morePageShow(data);
		});
		this.eventBus.$on('ic-page-more-click', data => {
			this.morePageShowClick(data);
		});
	},
	computed: {
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						if (row == 'icListClass1') {
							classArray.push('bot_list_text');
						} else if (row == 'icListClass2') {
							classArray.push('bot_btnset w-100p align_center');
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
		btn: function() {
			if (this.attribute) {
				if (this.attribute.btn) {
					return String(this.attribute.btn).toLowerCase() === 'true'
						? true
						: false;
				}
			}
			return false;
		},
		contText: function() {
			let text = [];
			if (this.attribute) {
				if (this.attribute.cont) {
					text = this.attribute.cont.split('%n');
				}
			}
			return text;
		},
	},
	mounted() {
		this.eventBus.$on('ic-page-carousel', data => {
			// alert('ic-page-carousel');
			this.setCarousel(data);
		});
	},
	methods: {
		setCarousel(data = {}) {
			if (this.idx == data.idx) {
				this.carouselItems = [];
				if (data.carouselItem && data.carouselItem.length > 0) {
					let list = data.carouselItem;
					let cnt = list.length / data.pageCount;
					let tempLists = [];
					for (var i = 0; i < cnt; i++) {
						tempLists.push({
							id: this.idx + '_' + i,
							items: list.splice(0, data.pageCount),
							divClass: this.divClass,
							class: this.class,
							colgroup: this.colgroup,
						});
					}
					this.carouselItems = tempLists;
				}
			}
		},
		morePageShow(data = {}) {
			if (this.idx == data.idx) {
				this.pageShowNum = data.pageShowNum;
			}
		},
		morePageShowClick(data = {}) {
			if (this.idx == data.idx) {
				this.pageShowNum = data.pageShowNum;
			}
		},
	},
};
</script>
