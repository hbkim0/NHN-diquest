<!-- 캐로셀 컴포넌트 -->
<template>
	<div>
		<carousel
			:id="this.id"
			:ref="`carousel_${this.id}`"
			:class="this.class"
			:margin="10"
			:auto-width="attribute.autoWidth != null ? attribute.autoWidth : true"
			:nav="attribute.nav"
			:dots="attribute.dots"
			:items="1"
			:nav-text="['<', '>']"
			@changed="carouselChanged"
			@updated="carouselUpdated"
		>
			<slot />
		</carousel>
		<!-- :items="0" -->
	</div>
</template>
<script>
import carousel from 'vue-owl-carousel';
export default {
	name: 'IcAnsCarousel',
	components: { carousel },
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
						// element에 id를 부여하여 구분할 때 사용
						type: String,
						default: null,
					},
					class: {
						// css와 같이 element에 공통으로 style을 적용할 때 사용
						type: Object,
						default: null,
					},
					nav: {
						type: Boolean,
						default: false,
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
					autoWidth: {
						// 자동넓이
						type: Boolean,
						default: false,
					},
				};
			},
		},
	},
	data() {
		return {
			test: {},
		};
	},
	computed: {
		id: function() {
			return 'carousel_' + this._uid;
		},
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.dots) {
					if (this.attribute.dots) {
						classArray.push('show-dots');
					}
					// class
				}
				if (this.attribute.class) {
					this.attribute.class.split(' ').forEach(row => {
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
	created() {
		this.eventBus.$on('ic-component-button-close', data => {
			this.componentButtonClose(data);
		});
	},
	mounted() {
		setTimeout(() => {
			this.owlStageHeight(0);
		}, 10);
	},
	methods: {
		componentButtonClose(data) {
			if (!this.test[data.idx]) {
				this.test[data.idx] = 0;
			}
			this.test[data.idx] += 1;
			if (
				document.getElementById(this.id) &&
				document.getElementById(this.id).getAttribute('idx') == data.idx
			) {
				if (
					document
						.getElementById(this.id)
						.getElementsByClassName('owl-stage')[0].childNodes.length ==
					this.test[data.idx]
				) {
					document
						.getElementById(this.id)
						.getElementsByClassName('owl-nav')[0].className += ' disabled';
					document
						.getElementById(this.id)
						.getElementsByClassName('owl-dots')[0].className += ' disabled';
				}
			}
		},
		owlStageHeight(index) {
			console.log(index);
			let elCarousel = document.getElementById(this.id);
			if (elCarousel) {
				try {
					let elItem = elCarousel.getElementsByClassName('item');
					let elOwlItem = elCarousel.getElementsByClassName('owl-item');
					if (elItem) {
						let height = 0;

						console.log(elItem.length);
						if (0 < elOwlItem.length) {
							document
								.getElementById(this.id)
								.getElementsByClassName(
									'owl-stage',
								)[0].style.width = `${(elOwlItem[0].clientWidth + 10) *
								elOwlItem.length}px`;
						}

						for (let i = 0; i < elItem.length; i++) {
							let elTextCont = elItem[i].getElementsByClassName('text_cont');
							if (elTextCont) {
								let elTextContStyle = elTextCont[0].style;
								elTextContStyle.setProperty('height', 'auto');
								if (height < elTextCont[0].offsetHeight) {
									height = elTextCont[0].offsetHeight;
								}
							}
						}
						for (let i = 0; i < elItem.length; i++) {
							let elTextCont = elItem[i].getElementsByClassName('text_cont');
							if (elTextCont) {
								let elTextContStyle = elTextCont[0].style;
								elTextContStyle.setProperty('height', height + 'px');
							}
						}
					}
				} catch (e) {
					console.log(e);
				}
			}
			// text_cont
			/*
      if (document.getElementById("my_status_list_" + index)) {
        let height = document.getElementById("my_status_list_" + index)
          .clientHeight;
        let el = document.getElementsByClassName("owl-stage-outer")[0];
        el.style.height = height + 8 + "px";
			}
			*/
		},
		carouselChanged(event) {
			this.owlStageHeight(event.item.index);
		},
		carouselUpdated(event) {
			console.log(event);
		},
	},
};
</script>
<style>
/*.show-dots .owl-carousel .owl-dots.disabled {
	display: block;
}*/
</style>
