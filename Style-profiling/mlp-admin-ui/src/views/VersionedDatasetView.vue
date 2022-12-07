<template>
  <v-card>
    <v-row>
      <v-col class="pa-5 pb-0" cols="10">
        <v-container row fluid>
          <v-col cols="4" style="max-width:300px;">
            <v-select 
              clearable
              outlined
              dense
              label="ML Task"
              :items="mlTask" 
              v-model="select.mlTask"
              @change="fetchDatasets"
            ></v-select>
          </v-col>
          <v-col cols="4" style="max-width:350px;">
            <v-select 
              clearable
              outlined 
              dense
              label="Dataset"
              v-model="select.dataset"
              :items="datasets"
              item-text="name"
              item-value="_id"
              @change="fetchVersionedDatasets"
            ></v-select> 
          </v-col>
          <v-col cols="4" style="max-width:250px;">
            <v-select 
              clearable
              outlined 
              dense
              label="Status"
              :items="status"
              v-model="select.status"
              @change="fetchVersionedDatasets"
            ></v-select>
          </v-col>
        </v-container>
      </v-col>
      <v-col class="pa-7 pb-0" cols="2">
        <v-btn 
          large 
          color="primary" 
          class="float-right"
          :to="{name: 'VersionedDatasetGenerateView'}"
        >GENERATE</v-btn>
      </v-col>
    </v-row>
    <v-row class="ma-7">
      <v-col
          class="pa-5" 
          v-for="(versionedDataset,index) in versionedDatasets" 
          :key="index"
          cols="12"
          md="6"
      >
        <v-card hover :to="{name: 'VersionedDatasetDetailView', params: {versioneddataset_id: versionedDataset._id}}">
          <div>
            <v-container row fluid>
              <v-col class="pa-0">
                <v-card-text class="pb-0 pt-0">
                  {{ getMLTaskName(versionedDataset.ml_task) }} > <b>{{ versionedDataset.dataset_name }}</b>
                </v-card-text>    
              </v-col>
              <v-col class="pa-0 text-right">
                <v-icon size="45">
                  {{ {...status.find((r => r.value === versionedDataset.status))}.icon }}
                </v-icon>
              </v-col>
            </v-container>
            <div class="d-flex">
              <div class="pa-0 ma-0">
                <v-footer color="white" padless style="height:100%;">
                  <v-card-title class="pt-0">
                    {{ versionedDataset.name }}
                  </v-card-title>
                  
                  <v-card-text>
                    Version {{ versionedDataset.index }} Generated {{ dayjs(versionedDataset.reg_date).format('YYYY-MM-DD') }}
                  </v-card-text>
                  <v-card-subtitle class="grey--text">
                    {{ versionedDataset.split }}
                  </v-card-subtitle>
                </v-footer>
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="10">
          <v-pagination
              v-model="pagenation.page"
              :length="pagenation.length"
              :total-visible="10"
              @input="pageMove"
          ></v-pagination>
      </v-col>
      <v-col cols="2" class="pr-10 d-flex justify-end">
          <v-select
              v-model="select.limit"
              :items="[10,20,50]"
              dense
              outlined
              hint="per page"
              persistent-hint
              @change="fetchVersionedDatasets"
              style="max-width:150px;"
          ></v-select>
      </v-col>   
    </v-row>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  data: () => ({
    versionedDatasets: [],
    datasets: [],
    versionedDatasetDialog: {
      show: false,
    },
    createDto: {
      ml_task: null,
      name: '',
      description: '',
      valid: true,
    },
    mlTask: [
      { text : 'TEXT DEEP TAGGING', value: 0 },
      { text : 'IMAGE DEEP TAGGING', value: 1 },
      { text : 'VIRTUAL TRY-ON', value: 2 },
    ],
    status: [
      { text : 'queued', value: 0 , icon: 'mdi-clipboard-text-clock-outline'},
      { text : 'processing', value: 1, icon: 'mdi-clipboard-play-outline' },
      { text : 'done', value: 2, icon: 'mdi-clipboard-check-outline' },
      { text : 'failed', value: 3, icon: 'mdi-clipboard-alert-outline' },
    ],
    select: {
      mlTask: null,
      dataset: null,
      status: null,
      limit: 10,
    },
    pagenation: {
      page : 1,
      length : 0,
    }
  }),
  computed: {
    ...mapGetters({
      fetchedVersionedDatasetViewFilter: 'fetchedVersionedDatasetViewFilter',
    })
  },
  created() {
    //필터 유지
    const route_params = this.$route.params;
    if(route_params.filterMaintain){
      this.select.limit = this.fetchedVersionedDatasetViewFilter.limit;
      this.select.dataset = this.fetchedVersionedDatasetViewFilter.dataset_id;
      this.select.status = this.fetchedVersionedDatasetViewFilter.status;
      this.select.mlTask = this.fetchedVersionedDatasetViewFilter.ml_task;
    }

    this.fetchDatasets();
  },
  methods: {
    fetchVersionedDatasets() {
      this.$store.dispatch('FETCH_VERSIONEDDATASETS', { ml_task: this.select.mlTask, dataset_id: this.select.dataset, status: this.select.status, sort_by: null, page: this.pagenation.page, limit: this.pagenation.limit })
        .then(res => {
          this.versionedDatasets = res.versionedDatasets;
          this.select.limit = res.limit;
          this.pagenation = res.pagenation;
        })
        .catch(error => { console.log(error); });
    },
    fetchDatasets() {
      this.$store.dispatch('FETCH_DATASETS', { ml_task: this.select.mlTask })
        .then(res => {
          this.datasets = res.datasets;
          this.fetchVersionedDatasets();
        })
        .catch(error => { console.log(error); });
    },
    pageMove(pageNum) {
      this.pagenation.page = pageNum;
      this.fetchDatasets();
    },
  }
}
</script>