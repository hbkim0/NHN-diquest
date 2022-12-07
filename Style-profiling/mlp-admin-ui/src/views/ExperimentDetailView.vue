<template>
  <v-card>
    <v-card-text class="text-h6">{{getMLTaskName(experiment.ml_task)}} > <b>{{experiment.dataset_name}}</b></v-card-text>
    <v-container fluid>
      <v-row>
        <v-col cols="auto">
          <v-card-text class="pt-2"><b>Name:</b></v-card-text>
        </v-col>
        <v-col cols="3">
          <v-form
            ref="form"
            lazy-validation
          >
            <v-container class="pa-0 ma-0" row v-if="editMode === false">
              <v-col cols="10" class="pr-0">
                <v-text-field
                  class="pa-0 ma-0"
                  readonly
                  dense
                  :value="experiment.name"
                  append-outer-icon="mdi-text-box-edit-outline"
                  @click:append-outer="editMode = true"
                >
                </v-text-field>
              </v-col>
            </v-container>
            <v-container row v-else>
              <v-col cols="10" class="pr-0">
                <v-text-field
                  class="pa-0 ma-0"
                  dense
                  clearable
                  :rules="[v => !!v || 'Required.']"
                  v-model="editExperimentDto.name"
                >
                </v-text-field>
              </v-col>
              <v-col class="pl-0">
                <v-icon
                  @click="save"
                  color="green"
                >
                  mdi-check
                </v-icon>
                <v-icon
                  @click="editMode = false; editExperimentDto.name = experiment.name;"
                  color="red"
                >
                  mdi-cancel
                </v-icon>
              </v-col>
            </v-container>
          </v-form>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="auto">
          <v-card-text>
            <strong>Status</strong> : {{ {...status.find((r) => r.value === experiment.status)}.text }}
          </v-card-text>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="auto">
          <v-card-text>
            <strong>Versioned Dataset</strong> : {{experiment.versioned_dataset_name}} (version {{experiment.versioned_dataset_index}}) 
            (<router-link v-if="experiment.versioned_dataset_id" :to="{name:'VersionedDatasetDetailView', params:{versioneddataset_id: experiment.versioned_dataset_id}}">detail...</router-link>)
          </v-card-text>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="auto">
          <v-card-text>
            <strong>Model</strong> : {{experiment.model_name}}
          </v-card-text>
        </v-col>
      </v-row>
      <v-row v-for="(algorithm, index) in experiment.algorithms" :key="index">
        <v-col>
          <v-card-text>
            <strong>Algorithm #{{index}} {{algorithm.name}}</strong>
          </v-card-text>
          <v-card-subtitle class="pt-0">Training arguments</v-card-subtitle>
          <template v-for="(params, pIndex) in algorithm.training_params">
            <v-card-subtitle :key="pIndex" class="pt-0">
              <v-container row fluid>
                <v-col cols="auto">
                  {{params.name}} (type: {{params.type}}) : 
                  {{
                      editExperimentDto.algorithms[index]['training_params'][pIndex]['argument'] !== null ? 
                      editExperimentDto.algorithms[index]['training_params'][pIndex]['argument'] :
                      params.default
                  }} 
                </v-col>
              </v-container>
            </v-card-subtitle>
          </template>
        </v-col>
      </v-row>
    </v-container>
    <v-card-actions class="justify-end">
      <v-btn
        v-if="experiment.status === 3 || experiment.status === 4"
        large
        color="warning"
        @click="dialog.show.deleteExperiment = true"
      >
        DELETE
      </v-btn>
      <v-btn
        large
        @click="moveExperimentView"
      >
        OK
      </v-btn>
      <v-btn
        v-if="experiment.status === 2 || experiment.status === 3"
        large 
        color="primary"
        @click="openTensorBoard"
      >
        TENSOR BOARD
      </v-btn>
    </v-card-actions>
    <v-dialog persistent width="500" v-model="dialog.show.deleteExperiment">
      <v-card>
        <v-card-title>Delete Experiment</v-card-title>
        <v-card-text>All-data in {{editExperimentDto.name}} will be deleted</v-card-text>
        <v-card-actions class="justify-end">
          <v-btn 
            large 
            @click="dialog.show.deleteExperiment = false"
          >CANCEL</v-btn>
          <v-btn 
            large 
            color="warning" 
            @click="deleteExperiment"
          >DELETE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    experiment: {},
    editExperimentDto: {
      name: null,
      algorithms: {},
    },
    editMode: false,
    dialog: {
        show: {
            deleteExperiment: false,
        }
    },
    status: [
      { text : 'created', value: 0 , icon: 'mdi-clipboard-plus-outline'},
      { text : 'queued', value: 1 , icon: 'mdi-clipboard-text-clock-outline'},
      { text : 'processing', value: 2, icon: 'mdi-clipboard-play-outline' },
      { text : 'done', value: 3, icon: 'mdi-clipboard-check-outline' },
      { text : 'failed', value: 4, icon: 'mdi-clipboard-alert-outline' },
    ],
  }),
  created() {
    this.fetchExperiment();
  },
  methods: {
    fetchExperiment() {
      this.$store.dispatch('FETCH_EXPERIMENT', this.$route.params.experiment_id)
        .then(res => {
          this.experiment = res;
          this.editExperimentDto.name = res.name;
          this.editExperimentDto.algorithms = res.algorithms;
        })
        .catch(error => { console.log(error) });
    },
    patchExperiment(params) {
      const validateForm = this.$refs.form.validate();
      if(!validateForm) {
        return;
      }

      this.$store.dispatch('PATCH_EXPERIMENT', params)
        .then(res => {
          this.experiment = res;
          this.editExperimentDto.name = res.name;
          this.editMode = false;
        })
        .catch(error => { console.log(error) });    
    },
    deleteExperiment() {
      this.$store.dispatch('DELETE_EXPERIMENT', this.$route.params.experiment_id)
        .then(res => {
          console.log(res);
          this.moveExperimentView();
        })
        .catch(error => { console.log(error) });  
    },
    save() {
      const params = { editExperimentDto: {...this.editExperimentDto, status: this.experiment.status}, experiment_id: this.$route.params.experiment_id };
      console.log('save - params', params);
      this.patchExperiment(params);
    },

    moveExperimentView() {
      this.$router.push({name: 'ExperimentView'});  
    },
    openTensorBoard() {
      this.$store.dispatch('CREATE_TENSORBOARD_URL', this.$route.params.experiment_id)
        .then(res => {
          if (res.status === 200) {
            console.log('ExperimentDetailView - TensorBoard Url - ', res.url);
            window.open(res.url);
          }
        })
        .catch(error => { console.log(error) });
      
    }
  }
}
</script>