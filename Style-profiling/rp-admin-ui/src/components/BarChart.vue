<template>
  <v-container fluid>
    <Bar
      :chart-options="chartOptions"
      :chart-data="chartData"
      :chart-id="chartId"
      :dataset-id-key="datasetIdKey"
      :plugins="plugins"
      :css-classes="cssClasses"
      :styles="styles"
      :width="width"
      :height="height"
    />
    <v-btn-toggle v-model="toggleScale" color="blue lighten-2">
      <v-btn 
        value="logarithmic" 
      >
        LogarithmicScale
      </v-btn>
    </v-btn-toggle>
  </v-container>
</template>

<script>
import { Bar } from 'vue-chartjs/legacy'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LogarithmicScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, LogarithmicScale)

export default {
  name: 'BarChart',
  components: {
    Bar
  },
  props: {
    chartData: {
      type: Object,
      default: () => {}
    },
  },
  data: () => ({
    toggleScale: null,
    chartId: 'bar-chart',
    datasetIdKey: 'label',
    width: 400,
    height: 400,
    cssClasses: '',
    styles: {},
    plugins: [],
    chartOptions: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          align: 'start',
        },
        tooltip: {
          callback: {},
        }
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
      scales: {
        x: {
          stacked: true,
          grid: {
            display: true,
          },
          title: {
            text: 'date',
            display: true,
          }
        },
        y: {
          stacked: true,
          type: 'linear',
          grid: {
            display: false,
          },
          title : {
            text: 'count',
            display: true,
          }
        }
      },  
    }
  }),
  watch: {
    'toggleScale' : 'changeScale',
  },
  methods: {
    changeScale() {
      if (this.toggleScale === 'logarithmic') {
        this.chartOptions.scales.y.type = this.toggleScale;
        this.chartOptions.scales.y.title.text = `count(log)`;
      } else {
        this.chartOptions.scales.y.type = 'linear';
        this.chartOptions.scales.y.title.text = `count`;
      }
    }
  }
}
</script>
