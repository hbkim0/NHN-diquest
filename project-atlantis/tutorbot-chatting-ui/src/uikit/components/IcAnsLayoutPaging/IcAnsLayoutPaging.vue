<!-- HTML 뷰어 컴포넌트 -->
<template>
	<div>
		<slot></slot>
		<div
			v-if="attribute.type == 'number'"
			class="mt-16 uikit-pagination"
			aria-label="Page navigation"
		>
			<page
				class="tui-pagination"
				:loading="page.loading"
				:page="page.current"
				:items-per-page="attribute.pageNo ? Number(attribute.pageNo) : 5"
				:total-items="page.total[idx]"
				:visible-pages="attribute.pagingNum ? Number(attribute.pagingNum) : 3"
				@beforeMove="onChangePage"
			/>
		</div>
		<div
			v-else-if="
				attribute.type == 'more' && pageNum < this.page.total[this.idx] - 1
			"
			class="bot_btnset align_center"
		>
			<button class="btn small gray type_square" @click="showMore()">
				<i class="fas fa-plus"></i><span>더보기</span>
			</button>
		</div>
	</div>
	<!--<div
		v-if="attribute.type == 'number'"
		class="mt-16 uikit-pagination"
		aria-label="Page navigation"
	>
		<page
			class="tui-pagination"
			:loading="page.loading"
			:page="page.current"
			:items-per-page="attribute.pageNo ? Number(attribute.pageNo) : 5"
			:total-items="page.total[idx]"
			:visible-pages="attribute.pagingNum ? Number(attribute.pagingNum) : 3"
			@beforeMove="onChangePage"
		/>
	</div>
	<div
		v-else-if="
			attribute.type == 'more' && pageNum < this.page.total[this.idx] - 1
		"
		class="bot_btnset align_center"
	>
		<button class="btn small gray type_square" @click="showMore()">
			<i class="fas fa-plus"></i><span>더보기</span>
		</button>
	</div>-->
</template>
<script>
import 'tui-pagination/dist/tui-pagination.css';
import { Pagination } from '../../components/lib/tui-pagination-vue';
export default {
	name: 'ic-ans-layout-paging',
	components: {
		page: Pagination,
	},
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
					type: {
						// paging방법결정
						type: String,
						default: null,
					},
					pageNo: {
						// 페이지당 아이템개수
						type: String,
						default: null,
					},
					pagingNum: {
						// type number일때 하단에 페이징숫자 노출개수
						type: String,
						default: null,
					},
					total: {
						// 총개수
						type: Number,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			pageNum: 0,
			page: {
				current: 1,
				total: {},
				perPage: 5,
				loading: true,
			},
		};
	},
	computed: {
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
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
		this.eventBus.$on('ic-table-count', data => {
			if (this.attribute.type == 'number') {
				if (this.idx == data.idx) {
					this.page.total[this.idx] = data.total;
					this.page.loading = false;
				}
			}
			if (this.attribute.type == 'more') {
				if (this.idx == data.idx) {
					this.page.total[this.idx] = data.total;
				}
			}
		});
	},
	mounted() {
		if (this.attribute.total) {
			this.page.total[this.idx] = this.attribute.total;
		}
		if (this.attribute.type == 'number') {
			this.eventBus.$emit('ic-page-count', {
				idx: this.idx,
				nodeId: this.nodeId,
				pageCount: Number(this.attribute.pageNo),
				current: this.page.current,
				total: this.attribute.total,
			});
		} else if (this.attribute.type == 'carousel') {
			this.eventBus.$emit('ic-page-carousel', {
				idx: this.idx,
				nodeId: this.nodeId,
				pageCount: Number(this.attribute.pageNo),
				current: this.page.current,
				carouselItem: this.attribute.carouselItem,
			});
		} else if (this.attribute.type == 'more') {
			this.eventBus.$emit('ic-page-more', {
				idx: this.idx,
				nodeId: this.nodeId,
				pageShowNum: Number(this.attribute.pageNo) - 1,
			});
			this.pageNum = Number(this.attribute.pageNo) - 1;
		}
	},
	methods: {
		showMore() {
			this.pageNum += Number(this.attribute.pageNo);
			this.eventBus.$emit('ic-page-more-click', {
				idx: this.idx,
				nodeId: this.nodeId,
				pageShowNum: this.pageNum,
			});
		},
		onChangePage(evt) {
			this.page.current = evt.page;
			this.eventBus.$emit('ic-page-change', {
				idx: this.idx,
				nodeId: this.nodeId,
				current: this.page.current,
			});
		},
	},
};
</script>
