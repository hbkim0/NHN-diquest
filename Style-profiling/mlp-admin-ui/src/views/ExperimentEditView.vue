<template>
  <v-card>
    <v-card-text class="text-h6">{{getMLTaskName(experiment.ml_task)}} > <b>{{experiment.dataset_name}}</b></v-card-text>
    <v-container fluid>
      <v-form
        ref="form"
        lazy-validation
      >
        <v-row>
          <v-col cols="auto">
            <v-card-text class="pt-2"><b>Name:</b></v-card-text>
          </v-col>
          <v-col cols="3">
            <v-text-field
              dense
              clearable
              :rules="[v => !!v || 'Required.']"
              v-model="editExperimentDto.name"
            >
            </v-text-field>
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
                    {{params.name}} (type: {{params.type}})
                  </v-col>
                  <v-col cols="auto" class="pt-1">
                    <v-text-field
                      v-if="params.type === 'integer'"
                      dense
                      type="number"
                      :rules="[(v) => !!v || 'required', (v) => v > 0 || 'value must be greater than 0']"
                      v-model.number="editExperimentDto.algorithms[index]['training_params'][pIndex]['argument']"
                    >
                    </v-text-field>
                    <v-text-field
                      v-else
                      dense                      
                      :rules="[(v) => !!v || 'required', (v) => v > 0 || 'value must be greater than 0']"
                      v-model="editExperimentDto.algorithms[index]['training_params'][pIndex]['argument']"
                    >
                    </v-text-field>
                  </v-col>
                  <v-col>
                    (default: {{params.default}})
                  </v-col>
                </v-container>
              </v-card-subtitle>
            </template>
          </v-col>
        </v-row>
      </v-form>
    </v-container>
    <v-card-actions class="justify-end">
      <v-btn
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
        CANCEL
      </v-btn>
      <v-btn
        large 
        color="primary" 
        @click="save"
      >
        SAVE
      </v-btn>
      <v-btn
        large 
        color="primary" 
        @click="saveAndTrain"
      >
          SAVE & TRAIN
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
    dialog: {
        show: {
            deleteExperiment: false,
        }
    }
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

          if(res.status !== 0){
            this.moveExperimentView();
          }
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
          console.log(res);
          this.moveExperimentView();
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
      const validateForm = this.$refs.form.validate();
    
      if(validateForm) {
        const params = { editExperimentDto: {...this.editExperimentDto, status: 0}, experiment_id: this.$route.params.experiment_id };
        this.patchExperiment(params);
      }
    },
    saveAndTrain() {
      const validateForm = this.$refs.form.validate();
    
      if(validateForm) {
        const params = { editExperimentDto: {...this.editExperimentDto, status: 1}, experiment_id: this.$route.params.experiment_id };
        this.patchExperiment(params);
      }
    },
    moveExperimentView() {
      this.$router.push({name: 'ExperimentView'});  
    }
  }
}
</script>