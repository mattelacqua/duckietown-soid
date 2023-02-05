// Import React
import React from "react";

// Import envInfo
import EnvInfo from "./EnvInfo.js"

// Import Buttons
import Buttons from './Buttons.js'

// Import Query Buttons
import Queries from '../counterfactual/Queries.js'
// Agent Component (gets rendered in app)
class Environment extends React.Component {

  // Construct it with state so we can keep track of relevant information
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

  // Render the Env component EnvInfo.js)
  render() {
    return (
              <div>
                {/* Render Environment Information */}
                <Buttons  sim_state={this.state.sim_state} 
                    update_from_sim={this.update_from_sim}
                    env_info={this.state.env_info}
                    socket={this.state.socket}/>

                <EnvInfo    max_NS={this.state.max_NS}
                            max_EW={this.state.max_EW}
                            sim_state={this.state.sim_state}
                            tile_size={this.state.tile_size}
                            sim_step={this.state.sim_step}/>

                <Queries  sim_state={this.props.sim_state} 
                  update_from_sim={this.props.update_from_sim}
                  env_info={this.props.env_info}
                  socket={this.props.socket}/>     
              </div>
          );
    }
}

// Allow it to be called in other functions
export default Environment;
