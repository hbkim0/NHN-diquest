<template>
  <v-card>
      <v-row>
        <v-col class="pa-7 pb-0" cols="7">
          <v-container row fluid>
            <v-col cols="auto">
              <v-select
                outlined
                clearable
                dense
                label="ML Task"
                :items="mlTask" 
                v-model="select.mlTask"
                @change="select.dataset = null; fetchDatasets();"
              ></v-select>
            </v-col>
            <v-col cols="auto">
              <v-select 
                clearable
                outlined
                dense
                label="Dataset"
                v-model="select.dataset"
                :items="datasets"
                item-text="name"
                item-value="_id"
                @change="fetchExperiments"
              ></v-select>
            </v-col>
            <v-col cols="auto">
              <v-select 
                clearable
                outlined 
                dense
                label="Status"
                v-model="select.status"
                :items="status"
                @change="fetchExperiments"
              ></v-select>
            </v-col>
          </v-container>
        </v-col>
        <v-col class="pa-7 pb-0 text-right">
          <v-btn 
            class="mr-2"
            large 
            color="primary" 
            @click="openExperimentDialog"
          >TRAINING</v-btn>
          <v-btn 
              class="mr-2"
              large 
              color="primary" 
              @click="dialog.show.tensorBoard = true"
          >TENSOR BOARD</v-btn>
        </v-col>
      </v-row>

      <v-row class="ma-7">
        <v-col
          class="pa-5" 
          v-for="(experiment,index) in experiments" 
          :key="index"
          cols="12"
          md="6"
        >
          <v-card hover :to="experiment.status === 0 ? {name: 'ExperimentEditView', params: {experiment_id: experiment._id}} : {name: 'ExperimentDetailView', params: {experiment_id: experiment._id}}">
            <div>
              <v-container row fluid>
                <v-col class="pa-0">
                  <v-card-text class="pb-0 pt-0">
                      {{ getMLTaskName(experiment.ml_task) }} > <b>{{ experiment.dataset_name }}</b>
                  </v-card-text>    
                </v-col>
                <v-col class="pa-0 text-right">
                  <v-icon size="45">
                    {{ {...status.find((r => r.value === experiment.status))}.icon }}
                  </v-icon>
                </v-col>
              </v-container>
              <div class="d-flex">
                <div class="pa-0 ma-0">
                  <v-footer color="white" padless style="height:100%;">
                    <v-card-title class="pt-0">
                      {{ experiment.name }}
                    </v-card-title>
                    <v-container row fluid>
                      <v-col cols="3" class="pl-5 pa-0">
                        <v-card-text class="pa-0 text-right">
                          Versioned:
                        </v-card-text>
                      </v-col>
                      <v-col cols="9" class="pl-5 pa-0">
                        <v-card-text class="pa-0">
                          {{experiment.versioned_dataset_name}} (Version {{ experiment.versioned_dataset_index }})
                        </v-card-text>
                      </v-col>
                      
                      <v-col cols="3" class="pl-5 pa-0">
                        <v-card-text class="pa-0 text-right">
                          Model:
                        </v-card-text>
                      </v-col>
                      <v-col cols="9" class="pl-5 pa-0">
                        <v-card-text class="pa-0">
                          {{ experiment.model_name }}
                        </v-card-text>
                      </v-col>
                    </v-container>
                    <v-card-subtitle class="grey--text">
                      {{ dayjs(experiment.mod_date).format('YYYY-MM-DD') }}
                    </v-card-subtitle>
                  </v-footer>
                </div>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
          <v-col cols="11">
              <v-pagination
                  v-model="pagenation.page"
                  :length="pagenation.length"
                  :total-visible="10"
                  @input="pageMove"
              ></v-pagination>
          </v-col>
          <v-col cols="1" class="pr-10">
              <v-select
                  v-model="select.limit"
                  :items="[10,20,50,100]"
                  dense
                  outlined
                  hint="per page"
                  persistent-hint
                  @change="fetchExperiments"
              ></v-select>
          </v-col>   
      </v-row>
      <v-dialog width="700" v-model="dialog.show.experiment">
        <v-form
          ref="form"
          lazy-validation
        >       
          <v-card>
            <v-card-title>Create Experiment</v-card-title>
            <v-row class="pa-0 ma-0">
              <v-col cols="auto">
                <v-card-subtitle class="pt-2">Dataset:</v-card-subtitle>
              </v-col>
              <v-col cols="auto">
                <v-select
                  outlined
                  clearable
                  dense
                  :rules="[v => !!v || 'Required.']"
                  label="Dataset"
                  v-model="createExperimentDiolog.dataset_id"
                  :items="datasets"
                  item-text="name"
                  item-value="_id"
                  @change="fetchVersionedDatasets"
                >
                </v-select>
              </v-col>
            </v-row>
            <v-row class="pa-0 ma-0">
              <v-col cols="auto">
                <v-card-subtitle class="pt-2">Versioned Dataset:</v-card-subtitle>
              </v-col>
              <v-col cols="auto">
                <v-select
                  outlined
                  clearable
                  dense
                  :rules="[v => !!v || 'Required.']"
                  label="Versioned Dataset"
                  :items="dialog.versionedDatasets"
                  item-text="name"
                  item-value="_id"
                  v-model="createExperimentDiolog.versioned_dataset_id"
                  @change="fetchModels"
                >
                </v-select>
              </v-col>
            </v-row>
            <v-row class="pa-0 ma-0">
              <v-col cols="auto">
                <v-card-subtitle class="pt-2">Model:</v-card-subtitle>
              </v-col>
              <v-col cols="auto">
                <v-select
                  outlined
                  clearable
                  dense
                  :rules="[v => !!v || 'Required.']"
                  label="Model"
                  v-model="createExperimentDiolog.model_id"
                  :items="dialog.models"
                  item-text="name"
                  item-value="_id"
                >
                </v-select>
              </v-col>
            </v-row>
            <v-row class="pa-0 ma-0">
              <v-col cols="auto">
                <v-card-subtitle class="pt-2">Name:</v-card-subtitle>
              </v-col>
              <v-col cols="7">
                <v-text-field
                  dense
                  clearable
                  :rules="[v => !!v || 'Required.']"
                  v-model="createExperimentDiolog.name"
                >
                </v-text-field>
              </v-col>
            </v-row>
            <v-card-actions class="justify-end">
              <v-btn
                @click="dialog.show.experiment = false; createExperimentDiolog={dataset_id: null,versioned_dataset_id: null,model_id: null,name: null,}"
              >
                CANCEL
              </v-btn>
              <v-btn
                color="primary"
                @click="createExperiment"
              >
                CREATE
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
      <v-dialog width="600" v-model="dialog.show.tensorBoard">
        <v-card>
          <v-card-title>Launch TensorBoard</v-card-title>
          <v-container class="pa-0 ma-0" row fluid style="height:60px;">
            <v-col cols="auto">
              <v-card-subtitle>Dataset :</v-card-subtitle>
            </v-col>
            <v-col cols="auto">
              <v-select
                outlined
                dense
                clearable
                label="Dataset"
                :items="datasets"
                item-text="name"
                item-value="_id"
                v-model="dialog.select.dataset"
                @change="fetchDialogExperiments"
              >
              </v-select>
            </v-col>
          </v-container>
          <v-container>
            <v-card class="rounded-lg">
              <v-virtual-scroll    
                :items="dialog.experiments"
                height="328"
                item-height="82"
              >
                <template v-slot:default="{ item }">
                  <v-list-item :key="item._id">
                    <v-list-item-content>
                      <v-list-item-title>
                        <strong>{{ item.name }}</strong>
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        Versioned Dataset : {{ item.versioned_dataset_name }}
                      </v-list-item-subtitle>
                      <v-list-item-subtitle>
                        Model : {{ item.model_name }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-checkbox
                        v-if="item.status === 3"
                        v-model="dialog.checkExperiment"
                        :value="item._id"
                      >
                      </v-checkbox>
                      <v-checkbox
                        v-else
                        disabled
                      >
                      </v-checkbox>
                    </v-list-item-action>
                  </v-list-item>
                    <v-divider></v-divider>
                </template>
              </v-virtual-scroll>
            </v-card>
          </v-container>
          <v-card-actions class="justify-end">
            <v-btn
              @click="dialog.show.tensorBoard = false; dialog.checkExperiment = [];"
            >
              CANCEL
            </v-btn>
            <v-btn
              color="primary"
              @click="launchTensorBoard"
            >
              LAUNCH
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  data: () => ({
    datasets: [],
    experiments: [],
    pagenation: {
      page : 1,
      length : 0,
    },
    status: [
      { text : 'created', value: 0 , icon: 'mdi-clipboard-plus-outline'},
      { text : 'queued', value: 1 , icon: 'mdi-clipboard-text-clock-outline'},
      { text : 'processing', value: 2, icon: 'mdi-clipboard-play-outline' },
      { text : 'done', value: 3, icon: 'mdi-clipboard-check-outline' },
      { text : 'failed', value: 4, icon: 'mdi-clipboard-alert-outline' },
    ],
    mlTask: [
      { text : 'TEXT DEEP TAGGING', value: 0 },
      { text : 'IMAGE DEEP TAGGING', value: 1 },
      { text : 'VIRTUAL TRY-ON', value: 2 },
    ],
    select: {
      mlTask: null,
      dataset: null,
      status: null,
      limit: 10,
    },
    dialog: {
      show: {
        experiment: false,
        tensorBoard: false,
      },
      select: {
        dataset: null,
      },
      checkExperiment: [],
      versionedDatasets: [],
      models: [],
      datasets: [],
      experiments: [],
    },
    createExperimentDiolog: {
      dataset_id: null,
      versioned_dataset_id: null,
      model_id: null,
      name: null,
    },
  }),
  computed: {
    ...mapGetters({
      fetchedExperimentViewFilter: 'fetchedExperimentViewFilter',
    })
  },
  created() {
    //필터 유지
    const route_params = this.$route.params;
    if(route_params.filterMaintain){
      this.select.mlTask = this.fetchedExperimentViewFilter.ml_task;
      this.select.dataset = this.fetchedExperimentViewFilter.dataset_id;
      this.select.status = this.fetchedExperimentViewFilter.status;
      this.select.limit = this.fetchedExperimentViewFilter.limit;
    }

    this.fetchDatasets();
    this.fetchDialogDatasets();
  },
  methods: {
    createExperiment() {
      const validateForm = this.$refs.form.validate();
    
      if(validateForm) {
        this.$store.dispatch('CREATE_EXPERIMENT', this.createExperimentDiolog )
          .then(res => {
            this.$router.push({name: 'ExperimentEditView', params: {experiment_id: res._id}})
          })
          .catch(error => { console.log(error); });
      }
    },
    fetchDatasets() {
      this.$store.dispatch('FETCH_DATASETS', { ml_task: this.select.mlTask })
        .then(res => {
          this.datasets = res.datasets;
          this.fetchExperiments();
        })
        .catch(error => { console.log(error); });
    },
    fetchExperiments() {
      this.$store.dispatch('FETCH_EXPERIMENTS', { ml_task: this.select.mlTask, dataset_id: this.select.dataset, status: this.select.status, sort_by: null, page: this.pagenation.page, limit: this.pagenation.limit })
        .then(res => {
          this.experiments = res.experiments;
          this.pagenation = res.pagenation;
        })
        .catch(error => { console.log(error); });
    },
    fetchVersionedDatasets() {
      this.$store.dispatch('FETCH_VERSIONEDDATASETS', { dataset_id: this.createExperimentDiolog.dataset_id, status: 2 })
        .then(res => {
          this.dialog.versionedDatasets = res.versionedDatasets;
          
        })
        .catch(error => { console.log(error); });
    },
    fetchModels() {
      const findMlTask = {...this.dialog.versionedDatasets.find((r) => r._id === this.createExperimentDiolog.versioned_dataset_id)}.ml_task;
      this.$store.dispatch('FETCH_MODELS', { ml_task: findMlTask })
        .then(res => {
          console.log('ExperimentView - fetchModels - res', res);
          this.dialog.models = res;
        })
        .catch(error => { console.log(error); });
    },
    pageMove(pageNum) {
      this.pagenation.page = pageNum;
      this.fetchExperiments();
    },
    openExperimentDialog() {
      this.dialog.show.experiment = true;
    },
    fetchDialogDatasets() {
      this.$store.dispatch('FETCH_DATASETS', {ml_task: null})
        .then(res => {
          this.dialog.datasets = res.datasets;
          this.fetchDialogExperiments();
        })
        .catch(error => { console.log(error); });
    },
    fetchDialogExperiments() {
      this.$store.dispatch('FETCH_EXPERIMENTS', { dataset_id: this.dialog.select.dataset })
        .then(res => {
          this.dialog.experiments = res.experiments;
        })
        .catch(error => { console.log(error); });
    },
    launchTensorBoard() {
      this.$store.dispatch('CREATE_TENSORBOARD_URL', this.dialog.checkExperiment)
        .then(res => {
          if (res.status === 200) {
            console.log('ExperimentView - TensorBoard Url - ', res.url);
            window.open(res.url);
          }
        })
        .catch(error => { console.log(error) });
    },
  }
}
</script>