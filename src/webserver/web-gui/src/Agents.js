// Import styplesheet for App
import './Agents.css';

// Import React for components
import React from 'react'

// Import Agents since it will be rendered in appb
import Agent from './Agent.js'


// Agent Component (gets rendered in app)
class Agents extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      agents: props.agents,
      socket: props.socket,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ 
      agents: nextProps.agents,
      socket: nextProps.socket,
    });
  }
 
  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    return (
                  this.state.agents.map((agent) => ( 
                    /* Render an Agent component, with props: agent_id, cur_angle, cur_pos, color */
                    <Agent agent_id={agent.agent_id} 
                           id={agent.id}
                           pos_x={agent.pos_x}
                           pos_z={agent.pos_z}
                           prev_pos_x={agent.prev_pos_x}
                           prev_pos_z={agent.prev_pos_z}
                           stop_x={agent.stop_x}
                           stop_z={agent.stop_z}
                           tile_x={agent.tile_x}
                           tile_z={agent.tile_z}
                           angle={agent.angle}
                           angle_deg={agent.angle_deg}
                           speed={agent.speed}
                           forward_step={agent.forward_step}
                           direction={agent.direction}
                           intersection_arrival={agent.intersection_arrival}
                           patience={agent.patience}
                           step_count={agent.step_count}
                           lookahead={agent.lookahead}
                           states={agent.state}
                           exists={agent.exists}
                           color={agent.color} 
                           turn_choice={agent.turn_choice} 
                           signal_choice={agent.signal_choice} 
                           lights={agent.lights} 
                           bbox_w={agent.bbox_w} 
                           bbox_l={agent.bbox_l} 
                           socket={this.state.socket} />
                    ))
          );
    }
}

// Allow it to be called in other functions
export default Agents;

