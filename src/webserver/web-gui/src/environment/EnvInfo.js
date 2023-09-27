import React from "react";


// Component to spit out agent information
class EnvInfo extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      max_NS: props.max_NS,
      max_EW: props.max_EW,
      tile_size: props.tile_size,
      sim_state: props.sim_state,
      sim_step: props.sim_step,
      run: (this.props.sim_state === 'run')
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({sim_state: nextProps.sim_state,
                   sim_step: nextProps.sim_step});
  }

  // Render the information to screen
  render() {
    let run = (this.props.sim_state === 'run')
    let std = (this.props.started === true)
    
    return (
      <div style={{
        display:'flex',
             flexDirection:'row',
             'pointer-events' : (run || !std) ? 'none' : 'auto',
             'opacity' : (run || !std) ? '0.5' : '1',
        }}>
          {/* HTML FOR ALL THE INFORMATION */}
          <p> Sim State: {this.state.sim_state.charAt(0).toUpperCase() + this.state.sim_state.slice(1)} &nbsp;|&nbsp; Sim Step: {Math.max(0, this.state.sim_step - 1)} </p>
      </div>
      );
    }
}


export default EnvInfo;
