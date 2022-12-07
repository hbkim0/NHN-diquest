import './assets/css/style.css';
import './assets/css/flatpickr.css';
import Lazy from './components/lib/lazy-loading/lazy';
import moment from 'moment';
import IcAnsMessage from './components/IcAnsMessage/IcAnsMessage';
import IcAnsMessageItem from './components/IcAnsMessage/IcAnsMessageItem';


export default {
  install(Vue) {

    Vue.prototype.moment = moment;

    const eventBus = Vue;
    Vue.prototype.eventBus = eventBus;
  
    // image-lazy-load
    const LazyClass = Lazy(Vue);
    const options = { throttleWait: 80 };
    const lazy = new LazyClass(options);
    Vue.prototype.$Lazyload = lazy;
  
    Vue.directive('lazy', {
      bind: lazy.add.bind(lazy),
      update: lazy.update.bind(lazy),
      componentUpdated: lazy.lazyLoadHandler.bind(lazy),
      unbind: lazy.remove.bind(lazy),
    });
  
    Vue.component(IcAnsMessage.name, IcAnsMessage);
    Vue.component(IcAnsMessageItem.name, IcAnsMessageItem);
    Vue.prototype.eventBus = new Vue();
  }
};
