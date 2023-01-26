// Import style
import './Agent.css';
// Import React
import React from "react";

// Import Agent Info Screen
import AgentInfo from './AgentInfo.js'

// Import Agent Query
import AgentQuery from './AgentQuery.js'

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
    return (
      <div>
        <AgentInfo  agent={this.props.agent} />

        <AgentQuery agent={this.props.agent}
                    socket={this.props.socket} />
    </div>
    );
  }
}

// Allow it to be called in other functions
export default Agent;
