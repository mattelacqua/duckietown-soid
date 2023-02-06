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

import './AgentMap.css'


ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

class AgentMap extends React.Component {

  // Constructor
  constructor(props) {
    super(props);

    this.update_agent_pos = this.update_agent_pos.bind(this);
    this.update_point_size = this.update_point_size.bind(this);

    this.state = {
      car_radius:0,
      is_dragging: false,
      socket: props.socket,
    }; // End state
  }

  update_agent_pos(e, datasetIndex, index, value) {
      e.target.style.cursor = 'default';
      console.log("Emitting agent_pos", value.x, value.y);
      console.log(index);
      console.log(value);
      this.state.socket.emit(
        'agent_pos',
        {
          'id': datasetIndex,
          'x': value.x,
          'z': value.y,
        });
      this.setState({is_dragging: false,});
  }

  update_point_size(chart, size){
    const area = size.width*size.height;
    const tile_area = this.props.tile_size * this.props.tile_size * 100000;
    const tile_scale = area / tile_area;
    const car_radius =  tile_scale * 1.5;
    this.setState({car_radius: car_radius});
  }

  // Check if we should update
  shouldComponentUpdate(nextProps, nextState) {
    if (nextState.is_dragging) {
      return false;
    } else {
      return true;
    }
  }

  render() {
    // Get Data
    let datasets = [];
    this.props.agents.forEach(function (agent) {
      datasets.push({
        label: agent.agent_id,
        data: [{x: agent.pos_x, y: agent.pos_z,}],
        backgroundColor: agent.color,
      });
    });
    let data = {
      datasets
    };
    
    // Load background image
    const image = new Image();
    image.src = 'http://localhost:5001/mapImage';

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
      }}
    };
    
    const options = {
      aspectRatio: 1,
      onResize: this.update_point_size,

      // Elements
      elements : {
        point : {
            radius : this.state.car_radius * 0.9, 
            pointStyle: 'rect',
        },
      },

      // Plugins
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        dragData: {
          dragX: true,
          round: 3,
          showTooltip: true,
          onDragStart:function (e, datasetIndex, index, value) {
            this.setState({is_dragging: true,});
          },
          onDrag: function (e, datasetIndex, index, value) {
            e.target.style.cursor = 'grabbing';

          },
          onDragEnd: this.update_agent_pos,
        }, // End drag Data
        legend: {
          position: 'bottom',
        },
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
          },
          type: "linear",

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

        <div classname='AgentMap'>
        <Line ref={this.chartReference} 
              classname="AgentMap" 
              options={options} 
              data={data} 
              width={550}
              height={550}
              plugins={[map_background]} 
              />
        </div>
    );
  }// End render
} // end component

export default AgentMap;

