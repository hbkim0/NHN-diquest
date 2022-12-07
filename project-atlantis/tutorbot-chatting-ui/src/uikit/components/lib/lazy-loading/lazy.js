/* eslint-disable no-unused-vars */
import {
	inBrowser,
	CustomEvent,
	remove,
	some,
	find,
	_,
	throttle,
	supportWebp,
	getDPR,
	scrollParent,
	getBestSelectionFromSrcset,
	assign,
	isObject,
	hasIntersectionObserver,
	modeType,
	ImageCache,
} from './util';

import ReactiveListener from './listener';
import 'intersection-observer';

const LOADING_IMG_URL =
	'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAARVBMVEXx8vSYmZqVlpf19viRkpPp6uy7vL7Cw8XW19m+v8Hv7/Hw8PLs7O+2t7ji4+Xf4OKpqqvKy82hoqOkpabR0dOwsbKMjY4UPJs7AAACz0lEQVR4nO3bjXKiMBSGYcgBsVgVUff+L7UgCOEvWMmOc9L3mZ12ttXMnG8h5oRsFAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABA6CT1K5dPV/Rrck/8Mmd1IXwnsV/mS18GhgyqDEweHQ6PP/0X+7v982j0+9GLJTNKMzh4G01vBrm30cgghAyktmk07RlImhXFcb+pAuUZyCUxlaTYcmfozqCKoP18v24YTXcGabdWSi7vF6E6A7n068Xyr2Zw7DPY8FmpO4O7lcH326PpziCzeqf3R1OdQXTqemizcxUhuWuTRHcG1oTguhXkmCR3x69VZ1BvKD2ugvjk+neupw3HCkJ5BpHcrlUCX85LvVlILd8t2jOoWqZD7uyZ5DlpJEtdhfoM1pXdvJnOvyD4DKxp01znCw09A7lZW9ALlQaegZwGO9DzU0LgGUTlcBd+9l1hZyC70YMIU8zUGnQGsp88jzLZtNigMhivE9KZx1HJ9MliQBlItB/WJ9fZR3KT0cLJQNI4GeytDjpr6264j8sNJ4M8rjujsvv7zGTQ3g3jrcdgMmj3lMzxWUw+n0D9mlGTGUoG3S57cmuqkWL5+Xw5HC2QDKz1oEnrciRzHNPoL5bmzWFk0DeHTWckZ+dJlefF0ggjA3uTvdkscSXQXSzPd4eQwaA5fHRG95XDOqYMLYPJenB+ZTAIwdpZCyEDKcclv3Bky2qjA8hg0hy+pn8wpT+DxfXgWgbdzpr+DN4+q9i10eozWGgOX/Fso7VnsNAcvqgbQ3MGK+vBFW0brTyD5ebwtRAuTW+hOYPV9eBqCPWUoDqDrmHeINKdwbbJoL0QqilBcwZ5/Diguc2/i2jO4LT3QvF10BzW9kJrBnHmT6E1g+1TQU/j/2eKfAZQ23Lc+UPkvPMr+3RFb/A3H7Y+XRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACA/+wH83QnC1gJfXYAAAAASUVORK5CYII=';
const ERROR_IMG_URL =
	'data:image/png;base64,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';
const DEFAULT_EVENTS = [
	'scroll',
	'wheel',
	'mousewheel',
	'resize',
	'animationend',
	'transitionend',
	'touchmove',
];
const DEFAULT_OBSERVER_OPTIONS = {
	rootMargin: '0px',
	threshold: 0,
};

export default function(Vue) {
	return class Lazy {
		constructor({
			preLoad,
			error,
			throttleWait,
			preLoadTop,
			dispatchEvent,
			loading,
			attempt,
			silent = true,
			scale,
			listenEvents,
			hasbind,
			filter,
			adapter,
			observer,
			observerOptions,
		}) {
			this.version = '__VUE_LAZYLOAD_VERSION__';
			this.mode = modeType.event;
			this.ListenerQueue = [];
			this.TargetIndex = 0;
			this.TargetQueue = [];
			this.options = {
				silent: silent,
				dispatchEvent: !!dispatchEvent,
				throttleWait: throttleWait || 200,
				preLoad: preLoad || 1.3,
				preLoadTop: preLoadTop || 0,
				error: error || ERROR_IMG_URL,
				loading: loading || LOADING_IMG_URL,
				attempt: attempt || 3,
				scale: scale || getDPR(scale),
				ListenEvents: listenEvents || DEFAULT_EVENTS,
				hasbind: false,
				supportWebp: supportWebp(),
				filter: filter || {},
				adapter: adapter || {},
				observer: !!observer,
				observerOptions: observerOptions || DEFAULT_OBSERVER_OPTIONS,
			};
			this._initEvent();
			this._imageCache = new ImageCache({ max: 200 });
			this.lazyLoadHandler = throttle(
				this._lazyLoadHandler.bind(this),
				this.options.throttleWait,
			);

			this.setMode(this.options.observer ? modeType.observer : modeType.event);
		}

		/**
		 * update config
		 * @param  {Object} config params
		 * @return
		 */
		config(options = {}) {
			assign(this.options, options);
		}

		/**
		 * output listener's load performance
		 * @return {Array}
		 */
		performance() {
			let list = [];

			this.ListenerQueue.map(item => {
				list.push(item.performance());
			});

			return list;
		}

		/*
		 * add lazy component to queue
		 * @param  {Vue} vm lazy component instance
		 * @return
		 */
		addLazyBox(vm) {
			this.ListenerQueue.push(vm);
			if (inBrowser) {
				this._addListenerTarget(window);
				this._observer && this._observer.observe(vm.el);
				if (vm.$el && vm.$el.parentNode) {
					this._addListenerTarget(vm.$el.parentNode);
				}
			}
		}

		/*
		 * add image listener to queue
		 * @param  {DOM} el
		 * @param  {object} binding vue directive binding
		 * @param  {vnode} vnode vue directive vnode
		 * @return
		 */
		add(el, binding, vnode) {
			if (some(this.ListenerQueue, item => item.el === el)) {
				this.update(el, binding);
				return Vue.nextTick(this.lazyLoadHandler);
			}

			let { src, loading, error, cors } = this._valueFormatter(binding.value);

			Vue.nextTick(() => {
				src = getBestSelectionFromSrcset(el, this.options.scale) || src;
				this._observer && this._observer.observe(el);

				const container = Object.keys(binding.modifiers)[0];
				let $parent;

				if (container) {
					$parent = vnode.context.$refs[container];
					// if there is container passed in, try ref first, then fallback to getElementById to support the original usage
					$parent = $parent
						? $parent.$el || $parent
						: document.getElementById(container);
				}

				if (!$parent) {
					$parent = scrollParent(el);
				}

				const newListener = new ReactiveListener({
					bindType: binding.arg,
					$parent,
					el,
					loading,
					error,
					src,
					cors,
					elRenderer: this._elRenderer.bind(this),
					options: this.options,
					imageCache: this._imageCache,
				});

				this.ListenerQueue.push(newListener);

				if (inBrowser) {
					this._addListenerTarget(window);
					this._addListenerTarget($parent);
				}

				this.lazyLoadHandler();
				Vue.nextTick(() => this.lazyLoadHandler());
			});
		}

		/**
		 * update image src
		 * @param  {DOM} el
		 * @param  {object} vue directive binding
		 * @return
		 */
		update(el, binding, vnode) {
			let { src, loading, error } = this._valueFormatter(binding.value);
			src = getBestSelectionFromSrcset(el, this.options.scale) || src;

			const exist = find(this.ListenerQueue, item => item.el === el);
			if (!exist) {
				this.add(el, binding, vnode);
			} else {
				exist.update({
					src,
					loading,
					error,
				});
			}
			if (this._observer) {
				this._observer.unobserve(el);
				this._observer.observe(el);
			}
			this.lazyLoadHandler();
			Vue.nextTick(() => this.lazyLoadHandler());
		}

		/**
		 * remove listener form list
		 * @param  {DOM} el
		 * @return
		 */
		remove(el) {
			if (!el) return;
			this._observer && this._observer.unobserve(el);
			const existItem = find(this.ListenerQueue, item => item.el === el);
			if (existItem) {
				this._removeListenerTarget(existItem.$parent);
				this._removeListenerTarget(window);
				remove(this.ListenerQueue, existItem);
				existItem.$destroy();
			}
		}

		/*
		 * remove lazy components form list
		 * @param  {Vue} vm Vue instance
		 * @return
		 */
		removeComponent(vm) {
			if (!vm) return;
			remove(this.ListenerQueue, vm);
			this._observer && this._observer.unobserve(vm.el);
			if (vm.$parent && vm.$el.parentNode) {
				this._removeListenerTarget(vm.$el.parentNode);
			}
			this._removeListenerTarget(window);
		}

		setMode(mode) {
			if (!hasIntersectionObserver && mode === modeType.observer) {
				mode = modeType.event;
			}

			this.mode = mode; // event or observer

			if (mode === modeType.event) {
				if (this._observer) {
					this.ListenerQueue.forEach(listener => {
						this._observer.unobserve(listener.el);
					});
					this._observer = null;
				}

				this.TargetQueue.forEach(target => {
					this._initListen(target.el, true);
				});
			} else {
				this.TargetQueue.forEach(target => {
					this._initListen(target.el, false);
				});
				this._initIntersectionObserver();
			}
		}

		/*
		 *** Private functions ***
		 */

		/*
		 * add listener target
		 * @param  {DOM} el listener target
		 * @return
		 */
		_addListenerTarget(el) {
			if (!el) return;
			let target = find(this.TargetQueue, target => target.el === el);
			if (!target) {
				target = {
					el: el,
					id: ++this.TargetIndex,
					childrenCount: 1,
					listened: true,
				};
				this.mode === modeType.event && this._initListen(target.el, true);
				this.TargetQueue.push(target);
			} else {
				target.childrenCount++;
			}
			return this.TargetIndex;
		}

		/*
		 * remove listener target or reduce target childrenCount
		 * @param  {DOM} el or window
		 * @return
		 */
		_removeListenerTarget(el) {
			this.TargetQueue.forEach((target, index) => {
				if (target.el === el) {
					target.childrenCount--;
					if (!target.childrenCount) {
						this._initListen(target.el, false);
						this.TargetQueue.splice(index, 1);
						target = null;
					}
				}
			});
		}

		/*
		 * add or remove eventlistener
		 * @param  {DOM} el DOM or Window
		 * @param  {boolean} start flag
		 * @return
		 */
		_initListen(el, start) {
			this.options.ListenEvents.forEach(evt =>
				_[start ? 'on' : 'off'](el, evt, this.lazyLoadHandler),
			);
		}

		_initEvent() {
			this.Event = {
				listeners: {
					loading: [],
					loaded: [],
					error: [],
				},
			};

			this.$on = (event, func) => {
				if (!this.Event.listeners[event]) this.Event.listeners[event] = [];
				this.Event.listeners[event].push(func);
			};

			this.$once = (event, func) => {
				const vm = this;
				function on() {
					vm.$off(event, on);
					func.apply(vm, arguments);
				}
				this.$on(event, on);
			};

			this.$off = (event, func) => {
				if (!func) {
					if (!this.Event.listeners[event]) return;
					this.Event.listeners[event].length = 0;
					return;
				}
				remove(this.Event.listeners[event], func);
			};

			this.$emit = (event, context, inCache) => {
				if (!this.Event.listeners[event]) return;
				this.Event.listeners[event].forEach(func => func(context, inCache));
			};
		}

		/**
		 * find nodes which in viewport and trigger load
		 * @return
		 */
		_lazyLoadHandler() {
			const freeList = [];
			this.ListenerQueue.forEach((listener, index) => {
				if (!listener.el || !listener.el.parentNode) {
					freeList.push(listener);
				}
				const catIn = listener.checkInView();
				if (!catIn) return;
				listener.load();
			});
			freeList.forEach(item => {
				remove(this.ListenerQueue, item);
				item.$destroy();
			});
		}
		/**
		 * init IntersectionObserver
		 * set mode to observer
		 * @return
		 */
		_initIntersectionObserver() {
			if (!hasIntersectionObserver) return;
			this._observer = new IntersectionObserver(
				this._observerHandler.bind(this),
				this.options.observerOptions,
			);
			if (this.ListenerQueue.length) {
				this.ListenerQueue.forEach(listener => {
					this._observer.observe(listener.el);
				});
			}
		}

		/**
		 * init IntersectionObserver
		 * @return
		 */
		_observerHandler(entries, observer) {
			entries.forEach(entry => {
				// if (entry.isIntersecting) {
				this.ListenerQueue.forEach(listener => {
					if (listener.el === entry.target) {
						if (listener.state.loaded)
							return this._observer.unobserve(listener.el);
						listener.load();
					}
				});
				// }
			});
		}

		/**
		 * set element attribute with image'url and state
		 * @param  {object} lazyload listener object
		 * @param  {string} state will be rendered
		 * @param  {bool} inCache  is rendered from cache
		 * @return
		 */
		_elRenderer(listener, state, cache) {
			if (!listener.el) return;
			const { el, bindType } = listener;

			let src;
			switch (state) {
				case 'loading':
					src = listener.loading;
					break;
				case 'error':
					src = listener.error;
					break;
				default:
					src = listener.src;
					break;
			}

			if (bindType) {
				el.style[bindType] = 'url("' + src + '")';
			} else if (el.getAttribute('src') !== src) {
				el.setAttribute('src', src);
			}

			el.setAttribute('lazy', state);

			this.$emit(state, listener, cache);
			this.options.adapter[state] &&
				this.options.adapter[state](listener, this.options);

			if (this.options.dispatchEvent) {
				const event = new CustomEvent(state, {
					detail: listener,
				});
				el.dispatchEvent(event);
			}
		}

		/**
		 * generate loading loaded error image url
		 * @param {string} image's src
		 * @return {object} image's loading, loaded, error url
		 */
		_valueFormatter(value) {
			let src = value;
			let loading = this.options.loading;
			let error = this.options.error;

			// value is object
			if (isObject(value)) {
				if (!value.src && !this.options.silent)
					console.error('Vue Lazyload warning: miss src with ' + value);
				src = value.src;
				loading = value.loading || this.options.loading;
				error = value.error || this.options.error;
			}
			return {
				src,
				loading,
				error,
			};
		}
	};
}
