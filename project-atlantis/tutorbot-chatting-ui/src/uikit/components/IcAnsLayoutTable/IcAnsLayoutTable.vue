<!-- 테이블 컴포넌트 -->
<template>
	<div>
		<template v-if="type == 'carousel' && computedCarouselItems">
			<ic-ans-carousel :attribute="this.carouselAttribute">
				<div
					v-for="carouselItem in computedCarouselItems"
					:key="carouselItem.id"
					class="item bot_tbl_wrap"
					:class="carouselItem.divClass"
					:style="attribute.style"
				>
					<table :class="carouselItem.class">
						<slot></slot>
						<template v-if="colgroup">
							<colgroup v-for="col in carouselItem.colgroup" :key="col.id">
								<col :style="col" />
							</colgroup>
						</template>
						<thead v-if="attribute.head != 'false'">
							<tr>
								<th v-if="attribute.checkbox" scope="col" style="width: 30px;">
									<label>
										<input type="checkbox" />
									</label>
								</th>
								<th v-for="rows in attribute.column" :key="rows.id" scope="col">
									{{ rows.name }}
								</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(row, i) in carouselItem.items" :key="row.id">
								<td v-if="attribute.checkbox" style="text-align: center;">
									<label>
										<input type="checkbox" />
									</label>
								</td>
								<template v-for="list in attribute.column" :class="list.align">
									<th
										v-if="list.id == 'th'"
										:key="list.apiColName + '_row_' + i"
									>
										<template v-if="list.url">
											<a
												:href="row.url"
												class="underline blue btn_bot_modal"
												@click.prevent.stop="onClickButton(row)"
												>{{ row[list.apiColName] }}</a
											>
											<template v-if="row.label">
												<br />
												{{ row.label }}
											</template>
										</template>
										<template v-else-if="list.checkbox">
											<label>
												<input type="checkbox" />
												{{ row[list.apiColName] }}
											</label>
										</template>
										<template v-else>{{ row[list.apiColName] }}</template>
									</th>
									<td
										v-else
										:key="list.apiColName + '_row_' + i"
										:class="{
											gray:
												attribute.class == 'icTableClass3' ||
												attribute.class == 'icTableClass4',
										}"
									>
										<template v-if="list.url">
											<a
												:href="row.url"
												class="underline blue btn_bot_modal"
												@click.prevent.stop="onClickButton(row)"
												>{{ row[list.apiColName] }}</a
											>
											<template v-if="row.label">
												<br />
												{{ row.label }}
											</template>
										</template>
										<template v-else-if="list.checkbox">
											<label>
												<input type="checkbox" />
												{{ row[list.apiColName] }}
											</label>
										</template>
										<div v-else v-html="row[list.apiColName]"></div>
									</td>
								</template>
							</tr>
						</tbody>
					</table>
				</div>
			</ic-ans-carousel>
		</template>
		<div
			v-else
			class="bot_tbl_wrap"
			:class="this.divClass"
			:style="attribute.style"
		>
			<table :class="this.class">
				<slot></slot>
				<template v-if="this.colgroup">
					<colgroup v-for="col in this.colgroup" :key="col.id">
						<col :style="col" />
					</colgroup>
				</template>
				<thead v-if="attribute.head != 'false'">
					<tr>
						<th v-if="attribute.checkbox" scope="col" style="width: 30px;">
							<label>
								<input type="checkbox" />
							</label>
						</th>
						<th v-for="rows in attribute.column" :key="rows.id" scope="col">
							{{ rows.name }}
						</th>
					</tr>
				</thead>
				<tbody>
					<tr
						v-for="(row, i) in computeItems.length > 0
							? computeItems[pageCurrent - 1]
							: attribute.items"
						:key="row.id"
						:style="pageShowNum && pageShowNum < i ? 'display:none' : ''"
					>
						<td v-if="attribute.checkbox" style="text-align: center;">
							<label>
								<input type="checkbox" />
							</label>
						</td>
						<template v-for="list in attribute.column" :class="list.align">
							<th
								v-if="list.id == 'th'"
								:key="list.apiColName + '_row_' + i"
								style="text-align:left"
							>
								<template v-if="list.url">
									<a
										:href="row.url"
										class="underline blue btn_bot_modal"
										@click.prevent.stop="onClickButton(row)"
										>{{ row[list.apiColName] }}</a
									>
									<template v-if="row.label">
										<br />
										{{ row.label }}
									</template>
								</template>
								<template v-else-if="list.checkbox">
									<label>
										<input type="checkbox" />
										{{ row[list.apiColName] }}
									</label>
								</template>
								<template v-else>{{ row[list.apiColName] }}</template>
							</th>
							<td
								v-else
								:key="list.apiColName + '_row_' + i"
								:class="{
									gray:
										attribute.class == 'icTableClass3' ||
										attribute.class == 'icTableClass4',
								}"
							>
								<template v-if="list.url">
									<a
										:href="row.url"
										class="underline blue btn_bot_modal"
										@click.prevent.stop="onClickButton(row)"
										>{{ row[list.apiColName] }}</a
									>
									<template v-if="row.label">
										<br />
										{{ row.label }}
									</template>
								</template>
								<template v-else-if="list.checkbox">
									<label>
										<input type="checkbox" />
										{{ row[list.apiColName] }}
									</label>
								</template>
								<div v-else v-html="row[list.apiColName]"></div>
							</td>
						</template>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>
<script>
import IcAnsCarousel from '../IcAnsCarousel';

export default {
	name: 'ic-ans-layout-table',
	components: {
		'ic-ans-carousel': IcAnsCarousel,
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
						// layout 식별하기 위한 id
						type: String,
						default: null,
					},
					class: {
						// css와 같이 element에 공통으로 style을 적용할 때 사용
						type: Object,
						default: null,
					},
					scroll: {
						// 스크롤 여부
						type: String,
						default: null,
					},
					divClass: {
						// div class
						type: String,
						default: null,
					},
					style: {
						// 스타일
						type: String,
						default: null,
					},
					checkbox: {
						// 체크박스
						type: Boolean,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			grid: {
				column: [],
			},
			pageCount: 0,
			pageCurrent: 1,
			pageShowNum: null,
			changedItems: [],
			carouselItems: null,
			carouselAttribute: {
				style: '',
				autoWidth: false,
				nav: false,
				dots: true,
			},
			carouselPageCount: 0,
			type: null,
		};
	},
	computed: {
		computedCarouselItems: function() {
			let itemArray = [];
			if (this.attribute.items && this.carouselPageCount > 0) {
				let list = this.attribute.items;
				let cnt = list.length / this.carouselPageCount;
				for (var i = 0; i < cnt; i++) {
					itemArray.push({
						id: this.idx + '_' + i,
						items: list.splice(0, this.carouselPageCount),
						divClass: this.divClass,
						class: this.class,
						colgroup: this.colgroup,
					});
				}
			}
			return itemArray;
		},
		computeItems: function() {
			let itemArry = [];
			if (this.attribute.items && this.pageCount > 0) {
				let list = this.attribute.items;
				let cnt = Math.floor(list.length / this.pageCount);

				for (var i = 0; i <= cnt; i++) {
					itemArry.push(list.splice(0, this.pageCount));
				}
			}
			return itemArry;
		},
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						if (row == 'icTableClass1') {
							classArray.push('bot_tbl_hover align_center bot_tbl01');
						} else if (row == 'icTableClass2') {
							classArray.push('bot_tbl_hover bot_tbl01');
						} else if (row == 'icTableClass3') {
							classArray.push(
								'td_p_b text_medium_small align_left align_top lh-12em mt-10px',
							);
						} else if (row == 'icTableClass4') {
							classArray.push(
								'td_p_b text_medium_small align_left align_top lh-12em mt-20px',
							);
						} else {
							classArray.push(row);
							classArray.push('bot_tbl01');
						}
					});
				} else {
					classArray.push('bot_tbl_hover bot_tbl01');
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
		divClass: function() {
			let dClass = '';
			if (this.attribute) {
				if (this.attribute.scroll) {
					if (this.attribute.scroll === 'on') {
						dClass = 'overflow_auto';
					} else {
						dClass = '';
					}
				}
				if (this.attribute.divClass) {
					dClass = this.attribute.divClass;
				}
			}
			return dClass;
		},
		colgroup: function() {
			let colArray = null;
			if (this.attribute) {
				if (this.attribute.colgroup) {
					colArray = this.attribute.colgroup.split(',');
				}
			}
			return colArray;
		},
	},
	created() {
		this.eventBus.$on('ic-page-count', data => {
			this.itemListChange(data);
		});
		this.eventBus.$on('ic-page-change', data => {
			this.changePage(data);
		});
		this.eventBus.$on('ic-page-more', data => {
			this.morePageShow(data);
		});
		this.eventBus.$on('ic-page-more-click', data => {
			this.morePageShowClick(data);
		});
	},
	mounted() {
		this.eventBus.$on('ic-page-carousel', data => {
			// alert('ic-page-carousel');
			this.setCarousel(data);
		});
		this.eventBus.$emit('ic-table-count', {
			idx: this.idx,
			nodeId: this.nodeId,
			total: this.attribute.items.length,
		});
	},
	methods: {
		setCarousel(data = {}) {
			if (this.idx == data.idx) {
				this.carouselPageCount = data.pageCount;
				this.type = 'carousel';
				/*this.carouselItems = [];
				this.type = 'carousel';
				if (this.attribute && this.attribute.items) {
					let list = this.attribute.items;
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
				}*/
			}
		},
		changePage(data = {}) {
			if (this.idx == data.idx) {
				this.pageCurrent = data.current;
			}
		},
		itemListChange(data = {}) {
			if (this.idx == data.idx) {
				this.pageCount = data.pageCount;
				this.pageCurrent = data.current;
				/*if (this.attribute && this.attribute.items) {
					this.changedItems = [];
					let list = this.attribute.items;
					let cnt = Math.floor(list.length / this.pageCount);

					for (var i = 0; i <= cnt; i++) {
						this.changedItems.push(list.splice(0, this.pageCount));
					}
				}*/
			}
		},
		owlStageHeight(index) {
			console.log(index);
		},
		carouselChanged(event) {
			this.owlStageHeight(event.item.index);
		},
		carouselUpdated(event) {
			console.log(event);
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
		onClickButton: function(row) {
			if (row.modal) {
				this.eventBus.$emit('ic-component-modal', {
					idx: this.idx,
					nodeId: this.nodeId,
					modalId: row.modal,
				});
				return;
			}
		},
	},
};
</script>
<style></style>
