import React from 'react';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-plugin-dragdata';

import io from 'socket.io-client';

import './AgentMap.css'

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

const socket = io();

class AgentMap extends React.Component {

  // Constructor
  constructor(props) {
    super(props);

    // Init Datasets
    const datasets = [];
    this.props.agents.forEach(function (agent) {
      datasets.push({
        label: agent.agent_id,
        data: [agent.cur_pos],
        backgroundColor: agent.color,
      });
    });

    this.update_agent_pos = this.update_agent_pos.bind(this);
    //
    // Init State
    this.state = {
      agents: this.props.agents,

      data:{datasets},
    }; // End state
    console.log(this.state.data);
  }

  update_agent_pos(e, datasetIndex, index, value) {
      e.target.style.cursor = 'default';
      socket.emit('agent_pos',
        {
          'id': "agent" + datasetIndex,
          'x': value.x,
          'z': value.y,
      });
      this.props.pos_pass("agent" + datasetIndex, value.x, value.y);
    }

  render() {
    // Load background image
    const image = new Image();
    image.src = 'http://localhost:5000/mapImage';
    console.log(image);

    const map_background = {
      beforeDraw: (chart) => {
      if (image.complete) {
          const ctx = chart.ctx;
          const {top, left, width, height} = chart.chartArea;
          console.log("chart");
          console.log(chart.height);
          console.log(chart.width);
          const x = left;
          const y = top;
          console.log("COMPLETE");
          ctx.drawImage(image, x, y, width, height);
        } else {
          image.onload = () => chart.draw();
          console.log("DRAW");
        }
      }
    };

    const options = {
          aspectRatio: 1,
          // Elements
          elements : {
            point : {
                radius : (2 * (20 * this.props.tile_size))
            },
          },
          // Plugins
          responsive: true,
          plugins: {
              dragData: {
                dragX: true,
                round: 3,
                showTooltip: true,
                onDragStart:function (e, datasetIndex, index, value) {},
                onDrag: function (e, datasetIndex, index, value) {
                    e.target.style.cursor = 'grabbing';
                },
                onDragEnd: this.update_agent_pos,
              }, // End drag Data
          }, // End plugin
          
          // Parsing
          parsing: {
              xAxisKey: 'x',
              yAxisKey: 'y',
          },

          // Scales x and y
          scales: {
            y: {
              dragData: true,
              beginAtZero: true,
              min : 0,
              max : this.props.max_NS,
              reverse : true,
              grid : {
                  color: 'LightGray',
              },
              ticks: {
                stepSize: this.props.tile_size,
              }

            }, // End y
            x: {
              dragData: true,
              beginAtZero: true,
              min : 0,
              max : this.props.max_EW,
              grid : {
                  color: 'LightGray',
              },
              ticks: {
                stepSize: this.props.tile_size,
              },
              type: "linear",
            }, // End x
          }, // End Scales
          
        }; // End options  

     return (
        <div classname = "AgentMap">
            <Line classname="agentMap" options={options} data={this.state.data} plugins={[map_background]} />;
        </div>
     )

  }
}

export default AgentMap;

