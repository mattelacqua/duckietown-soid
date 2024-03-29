// Import React
import React from "react";

// Import envInfo
//import EnvInfo from "./EnvInfo.js"

// Import envInfo
import LogStep from "./LogStep.js"

// Import Buttons
import StateButtons from './StateButtons.js'

// Import Environment style stuff
import './Environment.css'

// Agent Component (gets rendered in app)
class Environment extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {};
  }

  // Render the Env component EnvInfo.js)
  render() {
    return (
      <div className='Environment'>
        {/* Render Environment Information */}
        <StateButtons sim_state={this.props.sim_state}
                      update_from_sim={this.props.update_from_sim}
                      socket={this.props.socket}
                      started={this.props.started} />
        {/*
        <EnvInfo  sim_state={this.props.sim_state}
                  sim_step={this.props.sim_step}
                  started={this.props.started} />
         */}

        <LogStep  step={this.props.sim_step}
                  max_step={this.props.sim_step}
                  socket={this.props.socket}
                  sim_state={this.props.sim_state}
                  started={this.props.started} />
      </div>
    );
  }
}

// Allow it to be called in other functions
export default Environment;
