// Import style
import './Agent.css';
// Import React
import React from "react";

// Import Angle Dial 
import AngleDial from './AngleDial.js'

// Import Agent Info Screen
import AgentInfo from './AgentInfo.js'

// Import Info Screen
import LightDrop from './LightDrop.js'

// Import Delete Agent Button 
import DeleteAgent from './DeleteAgent.js'

// Import Turn Choice 
import TurnChoice from './TurnChoice.js'

// Agent Component (gets rendered in app)
class Agent extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      agent_id: props.agent_id,
      cur_pos: props.cur_pos,
      cur_angle: props.cur_angle,
      color: props.color,
      lights: props.lights,
      turn_choice: props.turn_choice,
      socket: props.socket,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ 
      agent_id: nextProps.agent_id,
      cur_pos: nextProps.cur_pos,
      cur_angle: nextProps.cur_angle,
      color: nextProps.color,
      lights: nextProps.light,
      turn_choice: nextProps.turn_choice,
      socket: nextProps.socket,
    });
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    return (
            <div>
                {/* Render a Dial */}
                <AngleDial  cur_angle={this.state.cur_angle} 
                            agent_id={this.state.agent_id} 
                            agent_color={this.state.color} 
                            angle_pass={this.angle_pass} 
                            socket={this.state.socket} />

                  {/* Render Agent Information */}
     
                <LightDrop  agent_id={this.state.agent_id} 
                            lights={this.state.lights}
                            lights_pass={this.lights_pass}
                            socket={this.state.socket} />
                <AgentInfo    agent_id={this.state.agent_id}
                              cur_angle={this.state.cur_angle}
                              cur_pos= {this.state.cur_pos}
                              color={this.state.color} 
                              turn_choice={this.state.turn_choice} 
                              lights={this.state.lights}/>
                <TurnChoice  agent_id={this.state.agent_id} 
                             turn_choice={this.state.turn_choice}
                             socket={this.state.socket} />
                <DeleteAgent  agent_id={this.state.agent_id}
                              socket={this.state.socket} />
             </div>
          );
    }
}

// Allow it to be called in other functions
export default Agent;
