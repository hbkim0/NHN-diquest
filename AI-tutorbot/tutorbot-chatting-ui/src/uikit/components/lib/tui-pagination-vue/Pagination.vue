<template>
	<nav class="mt-16" aria-label="Page navigation">
		<div ref="tuiPagination" />
	</nav>
</template>
<script>
import Pagination from 'tui-pagination'; /* ES6 */

const events = ['afterMove', 'beforeMove'];

export default {
	name: 'TuiPagination',
	props: {
		// Display page after pagination draw.
		page: {
			type: Number,
			required: true,
			default() {
				return 1;
			},
		},
		loading: {
			type: Boolean,
			default: false,
			required: false,
		},
		// Total item count
		totalItems: {
			type: Number,
			required: true,
			default() {
				return 10;
			},
		},
		// Item count per page
		itemsPerPage: {
			type: Number,
			default() {
				return 10;
			},
		},
		visiblePages: {
			type: Number,
			default() {
				return 3;
			},
			required: false,
		},
		// Option object
		options: {
			type: Object,
			default() {
				return {};
			},
		},
	},
	data() {
		return {
			instance: null,
		};
	},
	watch: {
		loading(loading) {
			this.setLoading(loading);
		},
		itemsPerPage(itemCount) {
			this.instance.setItemsPerPage(itemCount);
		},
		totalItems(itemCount) {
			this.instance.reset(itemCount);
			this.instance.movePageTo(this.page);
		},
	},
	mounted() {
		const el = this.$refs.tuiPagination;
		const options = Object.assign({}, this.options, {
			page: this.page,
			totalItems: this.totalItems,
			itemsPerPage: this.itemsPerPage,
			visiblePages: this.visiblePages,
		});

		this.instance = new Pagination(el, options);

		/*
    this.instance.on('beforeMove', (evt) => {
      alert('s');
      console.log(evt)
      this.$emit('beforeMove', evt)
    });
    */

		this.addEventListeners();
	},
	destroyed() {
		events.forEach(eventName => this.instance.off(eventName));
	},
	methods: {
		addEventListeners() {
			events.forEach(eventName => this.instance.off(eventName));
			events.forEach(eventName => {
				this.instance.on(eventName, (...args) => {
					if (eventName === 'beforeMove') {
						// eslint-disable-next-line no-empty
						if (this.loading) {
						} else {
							if (args[0].page != this.page) {
								this.$emit(eventName, ...args);
							}
						}
					} else {
						this.$emit(eventName, ...args);
					}
					return;
				});
			});
		},
		getRootElement() {
			return this.$refs.tuiPagination;
		},
		movePageTo(targetPage) {
			this.instance.movePageTo(targetPage);
			// scrollTo(0, 800)
		},
		getCurrentPage() {
			return this.instance.getCurrentPage();
		},
		reset(totalItems) {
			this.instance.reset(totalItems);
			scrollTo(0, 800);
		},
		setItemsPerPage(itemCount) {
			this.instance.setItemsPerPage(itemCount);
		},
		setTotalItems(itemCount) {
			this.instance.setTotalItems(itemCount);
		},
		setLoading(loading) {
			this.loading = loading;
		},
	},
};
</script>

<style>
/* code */
.uikit-pagination > .tui-pagination {
	font-size: 0;
	position: relative;
	margin: 20px 0;
}

.uikit-pagination > .tui-pagination .tui-page-btn {
	position: relative;
	width: 32px;
	height: 32px;
	background-color: #fff;
	font-size: 14px;
}

.uikit-pagination > .tui-pagination a.tui-page-btn {
	margin-left: -1px;
	border-width: 1px 1px;
	border-left: 1px solid #dee2e6 !important;
}

.uikit-pagination > .tui-pagination a.tui-page-btn.tui-next {
	margin-left: 10px;
}

.uikit-pagination > .tui-pagination .tui-first,
.uikit-pagination > .tui-pagination .tui-last,
.uikit-pagination > .tui-pagination .tui-next,
.uikit-pagination > .tui-pagination .tui-next-is-ellip,
.uikit-pagination > .tui-pagination .tui-prev,
.uikit-pagination > .tui-pagination .tui-prev-is-ellip {
	line-height: 30px;
	font-size: 0px !important;
}

.uikit-pagination > .tui-pagination .tui-is-selected,
.uikit-pagination > .tui-pagination strong {
	color: #fff !important;
	background: #909396 !important;
	border-color: #909396 !important;
	cursor: default;
}
</style>
