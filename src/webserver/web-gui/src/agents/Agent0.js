// Import style
import './Agent.css';
// Import React
import React from "react";

// Import Model Choice
import ModelChoice from './ModelChoice.js'

// Import Agent Info Screen
import AgentInfo from './AgentInfo.js'

// Import Angle Dial
import AngleDial from './AngleDial.js'

// Import Agent IntersectionArrival
import IntersectionArrival from './IntersectionArrival.js'

// Import Agent InitialDirection
import InitialDirection from './InitialDirection.js'

// Import Counterfactuals
import AddCounterfactual from './counterfactual/AddCounterfactual.js';
import CounterfactualList from './counterfactual/CounterfactualList.js'
import Queries from './counterfactual/Queries.js'

// Agent Component (gets rendered in app)
class Agent0 extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    let direction_label;
    if (this.props.agent.initial_direction === 0){
      direction_label = 'N'
    }
    else if (this.props.agent.initial_direction === 1){
      direction_label = 'S'
    }
    else if (this.props.agent.initial_direction === 2){
      direction_label = 'E'
    }
    else if (this.props.agent.initial_direction === 3){
      direction_label = 'W'
    }

    let agent = this.props.agent;

    let std = (this.props.started)

    return (
      <div className='Agent0'>
        <div className='Agent'>
          <div className='AgentMain' style={{width: '60%'}}>
            <div className='AgentHeader'>
              <h2> Agent {agent.agent_id.slice(-1)}. </h2>
              <ModelChoice agent={this.props.agents[0]} 
                           socket={this.props.socket}
                           started={this.props.started} />
            </div>
            {/* Manipulators */}
            <div className='AgentEdit'>
              <IntersectionArrival agents={this.props.agents}
                                   agent={agent}
                                   sim_step={this.props.sim_step}
                                   socket={this.props.socket} />
              <InitialDirection agent={agent}
                                direction_label={direction_label}
                                socket={this.props.socket} />
              <AngleDial  agent={agent}
                          socket={this.props.socket} />
            </div>
            <div className='AgentInfo'>
              <AgentInfo  agent={agent} />
            </div>
          </div>
          <div className="AgentCounterfactuals" class="card" style={{width: '30%', 'pointer-events' : (!std) ? 'none' : 'auto', 'opacity' : (!std) ? '0.5' : '1'}}>
            <AddCounterfactual  agent={agent} 
                                socket={this.props.socket} />
            <CounterfactualList agent={agent}  
                                socket={this.props.socket} />
          </div>
        </div>
        <Queries  socket={this.props.socket}
                  started={this.props.started}
                  update_from_sim={this.props.update_from_sim}
                  env_info={this.props.env_info} />
      </div>
    );
  }
}

// Allow it to be called in other functions
export default Agent0;
