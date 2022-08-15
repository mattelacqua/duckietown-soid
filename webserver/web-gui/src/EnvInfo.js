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
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({sim_state: nextProps.sim_state});
  }

  // Render the information to screen
  render() {
    return (
      <div>
          {/* HTML FOR ALL THE INFORMATION */}
          <p> Max NS: {this.state.max_NS}  Max EW: {this.state.max_EW} </p>
          <p> Tile Size: {this.state.tile_size} </p>
          <p> Sim State: {"" + this.state.sim_state} </p>
      </div>
      );
    }
}


export default EnvInfo;
