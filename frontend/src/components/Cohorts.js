import ApexCharts from 'apexcharts'
import axios from "axios";
import { useState, useEffect } from 'react';
import './Cohorts.css';


function Cohorts() {

    const API_ENDPOINT = "http://localhost:5050/api/cohorts"

    const [error, setError] = useState(false)
    const [sampleData, setSampleData] = useState([])



    useEffect(() => {
        const apiCall = async () => {
            try {


                const res = await axios.post(API_ENDPOINT)
                console.log(res)
                const sexs = res.data.response.collections[0].collectionEvents[0].eventGenders.distribution.genders
                const ethnicities = res.data.response.collections[0].collectionEvents[0].eventEthnicities.distribution.ethnicities
                const geoData = res.data.response.collections[0].collectionEvents[0].eventLocations.distribution.locations
                const diseasesData = res.data.response.collections[0].collectionEvents[0].eventDiseases.distribution.diseases

                console.log(geoData)

                const valuesSex = Object.values(sexs)
                const labelsSex = Object.keys(sexs)

                const valuesEthnicities = Object.values(ethnicities)
                const labelsEthnicities = Object.keys(ethnicities)

                const valuesGeo = Object.values(geoData)
                const labelsGeo = Object.keys(geoData)
                const entriesGeo = Object.entries(geoData)

                const valuesDiseases = Object.values(diseasesData)
                const labelsDiseases = Object.keys(diseasesData)

                var optionsSex = {

                    chart: {
                        type: 'donut'
                    },
                    title: {
                        text: 'Sex',
                    },
                    series: valuesSex,
                    labels: labelsSex,
                }

                var chartSex = new ApexCharts(document.querySelector("#chartSex"), optionsSex);
                chartSex.render();

                var optionsEthnicity = {
                    chart: {
                        type: 'bar'
                    },
                    title: {
                        text: 'Ethnicity',
                        align: 'center',
                        floating: true
                    },
                    series: [{
                        name: 'Number of individuals',
                        data: valuesEthnicities
                    }],
                    xaxis: {
                        categories: labelsEthnicities
                    }
                }

                var chartEthnicity = new ApexCharts(document.querySelector("#chartEthnicity"), optionsEthnicity);
                chartEthnicity.render()

                var optionsGeo = {

                    chart: {
                        type: 'pie'
                    },
                    title: {
                        text: 'Geographical origin',
                     
                    },
                    series: valuesGeo,
                    labels: labelsGeo,
                }

                var chartGeo = new ApexCharts(document.querySelector("#chartGeo"), optionsGeo);
                chartGeo.render()

        
                var optionsDiseases = {
                    series: [{
                    data: valuesDiseases
                  }],
                    chart: {
                    type: 'bar',
                    height: 700
                  },
                  plotOptions: {
                    bar: {
                      barHeight: '100%',
                      distributed: true,
                      horizontal: true,
                      dataLabels: {
                        position: 'bottom'
                      },
                    }
                  },
                  colors: ['#33b2df', '#546E7A', '#FFD700', '#2b908f', '#DC143C',
                    '#f48024', '#69d2e7', '#13d8aa', '#A5978B', '#f9a3a4', '#FF4500', '#51f08e', '#b051f0', 
                    '#CCFF33' , '#FF66CC' , '#FF3333', '#6633CC', '#CD853F' , '#3333FF' , '#FF3333'
                  ],
                  dataLabels: {
                    enabled: true,
                    textAnchor: 'start',
                    style: {
                      colors: ['#fff']
                    },
                    formatter: function (val, opt) {
                      return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
                    },
                    offsetX: 0,
                    dropShadow: {
                      enabled: true
                    }
                  },
                  stroke: {
                    width: 1,
                    colors: ['#fff']
                  },
                  xaxis: {
                    categories: labelsDiseases,
                  },
                  yaxis: {
                    labels: {
                      show: false
                    }
                  },
                  title: {
                      text: 'Diseases',
                      align: 'center',
                      floating: true
                  },
                  tooltip: {
                    theme: 'dark',
                    x: {
                      show: false
                    },
                    y: {
                      title: {
                        formatter: function () {
                          return ''
                        }
                      }
                    }
                  }
                  };

                var chartDiseases = new ApexCharts(document.querySelector("#chartDiseases"), optionsDiseases);
                chartDiseases.render()

            } catch (error) {
                setError(error)
                console.log(error)
            }
        }
        apiCall()
    }, [])

    return (<div className='chartsModule'><div id="chartSex"></div>
        <div id="chartGeo"></div>
        <div id="chartEthnicity"></div>
        <div id="chartDiseases"></div>

    </div>)

}

export default Cohorts