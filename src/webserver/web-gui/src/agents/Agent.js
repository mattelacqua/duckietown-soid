// Import style
import './Agent.css';
// Import React
import React from "react";

// Import Agent Info Screen
import AgentInfo from './AgentInfo.js'

// Import Angle Dial
import AngleDial from './AngleDial.js'

// Import Agent IntersectionArrival
import IntersectionArrival from './IntersectionArrival.js'

// Import Agent InitialDirection
import InitialDirection from './InitialDirection.js'

// Import Agent DeleteAgent
import DeleteAgent from './DeleteAgent.js'

// Import Agent DeleteAgent

// Agent Component (gets rendered in app)
class Agent extends React.Component {

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

    return (
      <div classname='Agent'>
        {/* Manipulators */}
          <AngleDial  agent={this.props.agent} 
                      socket={this.props.socket}
            />
          <IntersectionArrival agent={this.props.agent}
                              socket={this.props.socket} />

          <InitialDirection agent={this.props.agent}
                            direction_label={direction_label}
                            socket={this.props.socket} />
          

          {/* Information */}
          <AgentInfo  agent={this.props.agent} 
            />

          <DeleteAgent agent={this.props.agent}
                      socket={this.props.socket} 
            />
    </div>
    );
  }
}

// Allow it to be called in other functions
export default Agent;
