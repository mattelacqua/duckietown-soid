// Import React
import React from "react";

// Import envInfo
import EnvInfo from "./EnvInfo.js"

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
    this.state = {
    };
  }

  // Render the Env component EnvInfo.js)
  render() {
    return (
              <div classname='Environment'>
                {/* Render Environment Information */}
                <StateButtons sim_state={this.props.sim_state} 
                              update_from_sim={this.update_from_sim}
                              socket={this.props.socket}/>

                <EnvInfo  sim_state={this.props.sim_state}
                          sim_step={this.props.sim_step}/>

                <LogStep  step={this.props.sim_step}
                          max_step={this.props.sim_step}
                          socket={this.props.socket}/>
              </div>
          );
    }
}

// Allow it to be called in other functions
export default Environment;
