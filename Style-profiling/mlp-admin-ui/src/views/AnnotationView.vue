<template>
  <v-container fluid>
    <v-card  class="mt-10">
      <v-row class="ma-0">
        <v-col class="d-flex pt-5" cols="10">
          <v-row>
            <v-col sm="4" style="max-width:300px;">
              <v-select
                class="mx-2"
                dense
                outlined
                label="Dataset"
                item-text="name"
                item-value="_id"
                :items="datasets"
                v-model="selected.dataset"
                @change="fetchBundles"
                @click:clear="resetBundles"
              >
              </v-select>
            </v-col>
            <v-col sm="4" style="max-width:500px;">
              <v-select
                class="mx-2"
                multiple
                dense
                outlined
                small-chips
                clearable
                label="bundles"
                item-text="name"
                item-value="_id"
                :items="bundles"
                v-model="selected.bundles"
                @change="fetchAnnotations"
                @click:clear="fetchAnnotations"
              >
              </v-select>
            </v-col>
            <v-col sm="4" style="max-width:300px;">
              <v-select
                class="mx-2"
                dense
                outlined
                clearable
                label="labeled/unlabeled"
                :items="[{text:'labeled',value:1},{text:'unlabeled',value:0}]"
                v-model="selected.labeled"
                @change="fetchAnnotations"
                @click:clear="fetchAnnotations"
              >
              </v-select>
            </v-col>
          </v-row>
        </v-col>
        <v-col class="pa-5" cols="2">
          <v-btn 
            class="float-right"
            large 
            color="primary"
            @click="moveLabelingView"
          >ANNOTATE</v-btn>
        </v-col>
      </v-row>
      <v-container>
        <v-row dense>
          <v-col
            class="pa-5" 
            v-for="(anno,index) in annotations" 
            :key="index"
            style="max-width:19.7%;flex:0 0 19.7%;"
          >
            <v-card hover>
              <v-container
                v-if="anno.ml_task == 0"
                fluid
                class="pa-0 pt-5 text-center"
              >
                <v-card 
                  height="150"
                  width="220"
                  elevation="2"
                  class="mx-auto rounded-lg"
                  outlined
                  style="border-color:black;border-width:5px;"
                >
                  <v-card-text class="text-left d-inline-block text-truncate" style="max-width: 100%">{{anno.description}}</v-card-text>
                </v-card>
                <v-card-subtitle class="d-inline-block text-truncate" style="max-width: 100%">{{anno.file_name}}</v-card-subtitle>
                <v-divider></v-divider>
              </v-container>
              <v-img
                v-else
                :src="getCoverImage(anno.file_url)"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
              >
                <v-card-title class="d-inline-block text-truncate" style="max-width: 100%" v-text="anno.file_name"></v-card-title>
              </v-img>

              <v-card-actions>
                <!--done-->
                <v-icon color="green" v-if="anno.done === 1">
                  mdi-checkbox-marked-circle-outline
                </v-icon>
                <v-icon color="green" v-else-if="anno.done === 0 && anno.labels.length > 1">
                  mdi-tag-check-outline
                </v-icon>
                <v-icon color="red" v-else>
                  mdi-tag-remove-outline
                </v-icon>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <v-row>
        <v-col cols="10" class="px-0 mx-0">
          <v-pagination
            v-model="pagenation.page"
            :length="pagenation.length"
            :total-visible="10"
            @input="fetchAnnotations"
          ></v-pagination>
        </v-col>
        <v-col cols="2" class="pr-10 d-flex justify-end">
          <v-select
            v-model="selected.limit"
            :items="[10, 20, 50]"
            dense
            outlined
            hint="per page"
            persistent-hint
            @change="fetchAnnotations"
            style="max-width:120px;"
          ></v-select>
        </v-col> 
      </v-row>            
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    data: () => ({
      datasets: [],
      bundles: [],
      annotations: [],
      total_results: 0,
      pagenation: {
        page : 1,
        length : 0,
      },
      selected: {
        limit: 10,
        dataset: null,
        bundles: [],
        labeled: null,
      },
    }),
    computed: {
      ...mapGetters({
        fetchedAnnotationViewFilter: 'fetchedAnnotationViewFilter',
      })
    },
    created() {
      const route_params = this.$route.params;

      //필터 유지
      if(route_params.filterMaintain){
        this.selected.limit = this.fetchedAnnotationViewFilter.limit;
        this.selected.dataset = this.fetchedAnnotationViewFilter.dataset_id;
        this.selected.bundles = this.fetchedAnnotationViewFilter.bundle_id;
        this.selected.labeled = this.fetchedAnnotationViewFilter.labeled;
      } else { // Dataset Detail에서 넘어올경우
        this.selected.dataset = route_params.dataset_id != null ? String(route_params.dataset_id) : null;
        this.selected.bundles = route_params.selected_bundles != null ? route_params.selected_bundles : [];
        this.selected.labeled = route_params.selected_labeled != null ? route_params.selected_labeled : null;
      }

      this.fetchDatasets();
      
    },
    methods: {
      fetchDatasets() {
        this.$store.dispatch('FETCH_DATASETS', {})
          .then(res => {
            console.log('DatasetDetailView - created - fetch dataset',res);
            this.datasets = res.datasets;
            console.log(this.$route.params.dataset_id);
            // params dataset_id가 존재하지 않는 경우 dataset id 기본 0번 선택 
            if (typeof(this.$route.params.dataset_id) === 'undefined' && this.datasets.length > 0 && !this.$route.params.filterMaintain) {
              this.selected.dataset = this.datasets[0]._id;
            }
            this.fetchBundles();
          })
          .catch(error => {console.log(error)});      
      },
      fetchBundles() {
        this.$store.dispatch('FETCH_BUNDLES', this.selected.dataset)
        .then(res => {
          console.log('DatasetDetailView - created - fetch bundles',res);
          this.bundles = res.results;
          this.fetchAnnotations();
        })
        .catch(error => { console.log(error) });
      },
      fetchAnnotations() {
        const params = { 
          dataset_id : this.selected.dataset, 
          limit: this.selected.limit, 
          sort_by: null, 
          page: this.pagenation.page ,
          bundle_ids: this.selected.bundles,
          label_status: this.selected.labeled,
        };
        console.log('AnnotationView - fetch annotations - params',params);
        this.$store.dispatch('FETCH_ANNOTATIONS', params)
        .then(res => {
          console.log('AnnotationView - fetch annotations',res);
          this.pagenation = res.pagenation;
          this.selected.limit = res.limit;
          this.total_results = res.total_results;
          this.annotations = res.annotations;
        })
        .catch(error => { console.log(error) });
      },
      resetBundles() {
        this.bundles = [];
      },
      moveLabelingView() {
        const params = {
          dataset_id: this.selected.dataset,
          bundle_ids: this.selected.bundles,
          label_status: this.selected.labeled,
          total_results: this.total_results,
          ml_task: this.datasets.find(r => r._id === this.selected.dataset ).ml_task,
        };
        this.$router.push({name:'LabelingView', params: params});
      }
    }
}
</script>