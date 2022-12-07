import Vue from 'vue';

//
const eventBus = new Vue();

//
eventBus.$emitModal = (title, text) => {
  eventBus.$emit('show-modal', {title, text});
};

eventBus.$emitHomeModal = (title, _text) => {
  const text = _text || '홈페이지로 이동합니다.';
  const location = {name: 'home'};

  eventBus.$emit('show-modal', {title, text, location});
};

eventBus.$emitSnackbar = (title, text) => {
  eventBus.$emit('show-snackbar', {title, text});
};

//
Vue.prototype.$eventBus = eventBus;
