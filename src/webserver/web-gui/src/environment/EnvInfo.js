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
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({sim_state: nextProps.sim_state,
                   sim_step: nextProps.sim_step});
  }

  // Render the information to screen
  render() {
    return (
      <div style={{
        display:'flex',
        flexDirection:'row',
        }}>
          {/* HTML FOR ALL THE INFORMATION */}
          <p> Sim State: {this.state.sim_state} -</p>
          <p> --- Sim Step: {this.state.sim_step} </p>


      </div>
      );
    }
}


export default EnvInfo;
