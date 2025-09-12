import createVueApplication from 'utils/create-vue-application';
import IndexPage from '@//mariner_proj/index/IndexPage.vue';

createVueApplication(IndexPage).then(vueApp => {
  vueApp.mount('#app');
});
