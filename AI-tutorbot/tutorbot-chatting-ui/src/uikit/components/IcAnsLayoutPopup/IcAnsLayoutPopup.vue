<!-- 팝업 컴포넌트 -->
<template>
	<div
		v-if="isShow"
		class="chat_modal"
		:class="this.class"
		id="modal_sample1"
		style="display: block;"
		ref="attribute.id"
	>
		<template
			v-if="attribute.type && attribute.type.indexOf('emoticon') !== -1"
		>
			<button
				class="btn_modal_close fas fa-times type_blankfull"
				@click.prevent.stop="onClickButton('cancel')"
			>
				<span class="bg_clip">닫기</span>
			</button>
			<slot></slot>
		</template>
		<template v-else>
			<div class="chat_modal_in" :style="attribute.style">
				<div class="chat_modal_head">
					<div class="primary_c">
						<strong>{{ attribute.title }}</strong>
					</div>
					<button
						class="btn_modal_close fas fa-times"
						@click.prevent.stop="onClickButton('cancel')"
					>
						<span class="bg_clip">닫기</span>
					</button>
				</div>

				<ic-ans-modal>
					<slot></slot>
				</ic-ans-modal>

				<div class="chat_modal_foot">
					<div :class="this.ulClass">
						<button
							v-if="this.left"
							:class="this.leftClass"
							@click.prevent.stop="onClickButton()"
						>
							{{ this.left }}<i :class="attribute.leftIClass"></i>
						</button>
						<!-- 닫기 .btn_modal_close 추가 -->
						<button
							v-if="attribute.right"
							:class="this.rightClass"
							@click.prevent.stop="onClickButton('confirm')"
						>
							{{ attribute.right }}<i :class="attribute.rightIClass"></i>
						</button>
					</div>
				</div>
			</div>
		</template>
	</div>
</template>
<script>
import IcAnsModal from '../IcAnsModal';

export default {
	name: 'ic-ans-layout-popup',
	components: {
		'ic-ans-modal': IcAnsModal,
	},
	props: {
		idx: Number, // 메시지 번호
		nodeId: String, // 노드 식별자
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
					style: {
						// 스타일
						type: String,
						default: null,
					},
					leftClass: {
						type: Object,
						default: null,
					},
					rightClass: {
						type: Object,
						default: null,
					},
					leftIClass: {
						type: Object,
						default: null,
					},
					rightIClass: {
						type: Object,
						default: null,
					},
					left: {
						// 왼쪽버튼
						type: String,
						default: null,
					},
					right: {
						// 오른쪽버튼
						type: String,
						default: null,
					},
					title: {
						// 제목
						type: String,
						default: null,
					},
				};
			},
		},
	},
	computed: {
		class: function() {
			let classType = '';

			if (this.attribute) {
				if (this.attribute.type) {
					// class
					classType = this.attribute.type.replace('emoticon', '');
				}
			}
			return classType;
		},
		ulClass: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					let classList = this.attribute.class;
					if (this.attribute.hasOwnProperty('src')) {
						if (this.attribute.src.length == 0) {
							classList = this.attribute.class.replace('half', 'full');
						}
					}
					classList.split(' ').forEach(row => {
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
		leftClass: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.leftClass) {
					// class
					this.attribute.leftClass.split(' ').forEach(row => {
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
		rightClass: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.rightClass) {
					// class
					this.attribute.rightClass.split(' ').forEach(row => {
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
		leftIClass: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.leftIClass) {
					// class
					this.attribute.leftIClass.split(' ').forEach(row => {
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
		left: function() {
			let leftTxt = null;
			if (this.attribute) {
				if (this.attribute.left) {
					// class
					if (this.attribute.src) {
						if (this.attribute.src.length == 0) {
							leftTxt = null;
						} else {
							leftTxt = this.attribute.left;
						}
					} else {
						leftTxt = null;
					}
				}
			}

			return leftTxt;
		},
		rightIClass: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.rightIClass) {
					// class
					this.attribute.rightIClass.split(' ').forEach(row => {
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
	data() {
		return {
			isShow: false,
		};
	},
	mounted() {},
	methods: {
		onClickButton: function(tp) {
			if (tp == 'confirm') {
				this.eventBus.$emit('ic-component-ans-message-scroll', {
					scroll: true,
				});
				this.isShow = false;
			} else if (tp == 'cancel') {
				this.eventBus.$emit('ic-component-ans-message-scroll', {
					scroll: true,
				});
				this.isShow = false;
			} else {
				if (this.attribute.src) {
					if (!this.attribute.src.match(/^https?:\/\//i)) {
						this.attribute.src = 'http://' + this.attribute.src;
					}
					window.open(this.attribute.src, '_blank');
				} else {
					this.eventBus.$emit('ic-component-ans-message-scroll', {
						scroll: true,
					});
					this.isShow = false;
				}
			}
		},
	},
	created() {
		if (this.attribute.hasOwnProperty('src')) {
			if (this.attribute.src.length == 0) {
				this.attribute.left = '';
				if (this.attribute.class) {
					this.attribute.class = this.attribute.class.replace('half', 'full');
				}
			}
		}

		this.eventBus.$on('ic-component-modal', data => {
			console.log(data);
			if (data.modalId) {
				if (data.modalId == this.attribute.id && data.idx == this.idx) {
					if (this.isShow) {
						this.isShow = false;
						this.eventBus.$emit('ic-component-ans-message-scroll', {
							scroll: true,
						});
					} else {
						this.isShow = true;
						this.eventBus.$emit('ic-component-ans-message-scroll', {
							scroll: false,
						});
						document.getElementById('chat_wrapper').appendChild(this.$el);
					}
				}
			} else {
				if (data.idx == this.idx) {
					if (this.isShow) {
						this.isShow = false;
						this.eventBus.$emit('ic-component-ans-message-scroll', {
							scroll: true,
						});
					} else {
						if (!(data.close && data.close.toLowerCase() === 'true')) {
							this.isShow = true;
							this.eventBus.$emit('ic-component-ans-message-scroll', {
								scroll: false,
							});
							document.getElementById('chat_wrapper').appendChild(this.$el);
						}
					}
				}
			}
		});
	},
};
</script>
<style></style>
