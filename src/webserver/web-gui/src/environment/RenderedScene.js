import React from "react";
import LogStep from "./LogStep.js"


// Component to spit out agent information
class RenderedScene extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      src: "http://localhost:5001/renderedScene",
      key: Date.now(),
    };

    this.tick = this.tick.bind(this);
    this.error_tick = this.error_tick.bind(this);
  }

  tick() {
    this.setState({
      src: "http://localhost:5001/renderedScene",
      key: Date.now(),
    }) 
  }

  error_tick() {
    this.setState({
      src: "http://localhost:5001/renderedScene",
      key: Date.now(),
    });
  }

  componentDidMount() {
    this.interval = setInterval(() => this.tick(), 200);
  }
  
  // Render the information to screen
  render() {
    return (
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
          <img src={this.state.src + "?v=" + this.state.key} onError={this.error_tick} 
                style={{
                        display: 'float',
                        float: 'left',
                        height: '450px',
                        width: '600px',
                }} /> 
          <span> Rendered Scene </span>
          {this.props.sim_state === 'pause' &&
            <LogStep  step={this.props.sim_step}
                      max_step={this.props.sim_step}
                      socket={this.props.socket}/>
          }
      </div>
      
      );
    }
}


export default RenderedScene;
