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

import _ from 'lodash';

import './AgentMap.css'

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

const socket = io();

class AgentMap extends React.Component {

  // Constructor
  constructor(props) {
    super(props);

    this.update_agent_pos = this.update_agent_pos.bind(this);
    this.update_point_size = this.update_point_size.bind(this);
    //
    // Init State
    let datasets = [];
    this.props.agents.forEach(function (agent) {
      datasets.push({
        label: agent.agent_id,
        data: [agent.cur_pos],
        backgroundColor: agent.color,
      });
    });
    let new_agents = props.agents;
    this.state = {
      agents: new_agents,
      data:{datasets},

      car_radius:0,
    }; // End state

  }

  update_agent_pos(e, datasetIndex, index, value) {
      e.target.style.cursor = 'default';
      socket.emit('agent_pos',
        {
          'id': "agent" + datasetIndex,
          'x': value.x,
          'z': value.y,
      });
      this.props.pos_pass(datasetIndex, value.x, value.y);
    }

  update_point_size(chart, size){
    const area = size.width*size.height;
    const tile_area = this.props.tile_size * this.props.tile_size * 100000;
    const tile_scale = area / tile_area;
    const car_radius =  tile_scale * 1.5;
    this.setState({car_radius: car_radius});
  }

  componentWillReceiveProps(nextProps) {

    let datasets = [];
    nextProps.agents.forEach(function (agent) {
      datasets.push({
        label: agent.agent_id,
        data: [agent.cur_pos],
        backgroundColor: agent.color,
      });
    });
    this.setState({
      agents: nextProps.agents,
      data: datasets,
    });
  }


  

  render() {
    // Load background image
    const image = new Image();
    image.src = 'http://localhost:5000/mapImage';

    const map_background = {
      beforeDraw: (chart) => {
      if (image.complete) {
          const ctx = chart.ctx;
          const {top, left, width, height} = chart.chartArea;
          const x = left;
          const y = top;
          ctx.drawImage(image, x, y, width, height);
        } else {
          image.onload = () => {
          chart.draw();
          }
        }
      }
    };
    
    const options = {
          aspectRatio: 1,
          onResize: this.update_point_size,
          // Elements
          elements : {
            point : {
                radius : this.state.car_radius, 
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

     const style = {
       float: 'left',
       width: '50%',
     }
     return (
        <div classname = "AgentMap" style={style}>
            <Line ref={this.chartReference} classname="agentMap" options={options} data={this.state.data} plugins={[map_background]} />;
        </div>
     )

  }
}

export default AgentMap;

