import React from "react";

// Import Environment since it will be rendered in app
import Environment from './Environment.js'

// Component to spit out agent information
class RenderedScene extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      src: "http://localhost:5001/renderedScene",
      key: Date.now(),
      lst: Date.now(),
    };

    this.tick = this.tick.bind(this);
    this.error_tick = this.error_tick.bind(this);
  }

  tick() {
    this.setState({
      src: "http://localhost:5001/renderedScene",
      key: Date.now(),
      lst: this.state.lst,
    })
  }

  error_tick() {
    this.setState({
      src: "http://localhost:5001/renderedScene",
      key: Date.now(),
      lst: this.state.lst,
    });
  }

  load_tick() {
    this.setState({
      src: this.state.src,
      key: this.state.key,
      lst: this.state.key,
    })
  }

  componentDidMount() {
    this.interval = setInterval(() => this.tick(), 200);
  }
  
  // Render the information to screen
  render() {
    return (
      <div className="RenderedScene">
        <div
          style={{
                display: 'float',
                float: 'left',
                height: '450px',
                width: '600px',
                backgroundImage: "url('http://localhost:5001/mapImageBackground')",
                backgroundSize: "cover",
                background: "gray15",
              }}>
          
            {/* HTML FOR IMAGE */}
            <img src={this.state.src + "?v=" + this.state.key}
                 onLoad={() => { this.load_tick() }}
                 onError={(e) => { e.currentTarget.onerror = null; e.currentTarget.src = this.state.src + "?v=" + this.state.lst; this.error_tick() }}
                  style={{
                          display: 'float',
                          float: 'left',
                          height: '450px',
                          width: '600px',
                  }} /> 
        </div>
        <Environment  max_NS={this.props.max_NS} 
                      max_EW={this.props.max_EW}
                      tile_size={this.props.tile_size}
                      sim_state={this.props.sim_state}
                      socket={this.props.socket}
                      update_from_sim={this.props.update_from_sim}
                      sim_step={this.props.sim_step}
                      started={this.props.started} />
      </div>
      );
    }
}


export default RenderedScene;
