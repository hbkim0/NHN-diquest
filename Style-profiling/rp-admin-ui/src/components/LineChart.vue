<template>
  <v-container fluid>
    <LineChartGenerator
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
import { Line as LineChartGenerator } from 'vue-chartjs/legacy'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
  LogarithmicScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
  LogarithmicScale
)

export default {
  name: 'LineChart',
  components: {
    LineChartGenerator
  },
  props: {
    chartData: {
      type: Object,
      default: () => {}
    },
  },
  data: () => ({
    toggleScale: null,
    chartId: 'line-chart',
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
        }
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
      scales: {
        x: {
          //stacked: true,
          grid: {
            display: false,
          },
          title: {
            text: 'date',
            display: true,
          }
        },
        y: {
          //stacked: true,
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
