// Import React
import React from "react";

// Import Angle Dial 
import AngleDial from './AngleDial.js'

// Import Agent Info Screen
import AgentInfo from './AgentInfo.js'

// Agent Component (gets rendered in app)
class Agent extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      agent_id: props.agent_id,
      cur_pos: props.cur_pos,
      cur_angle: props.cur_angle,
      color: props.color
    };
  }


  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    return (
              <div>
                  {/* Render a Dial */}
                <AngleDial cur_angle={this.state.cur_angle} agent_id={this.state.agent_id} />

                  {/* Render Agent Information */}
                <AgentInfo    agent_id={this.state.agent_id}
                              cur_angle={this.state.cur_angle}
                              cur_pos= {this.state.cur_pos}
                              color={this.state.color} />
              </div>
          );
    }
}

// Allow it to be called in other functions
export default Agent;
