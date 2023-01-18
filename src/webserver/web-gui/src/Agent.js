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

// Import Signal Choice 
import SignalChoice from './SignalChoice.js'

// Import Forward Step 
import ForwardStep from './ForwardStep.js'

// Import Forward Step 
import BoundingBox from './BoundingBox.js'

// Agent Component (gets rendered in app)
class Agent extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      agent_id: props.agent_id,
      id: props.id,
      pos_x: props.pos_x,
      pos_z: props.pos_z,
      prev_pos_x: props.prev_pos_x,
      prev_pos_z: props.prev_pos_z,
      stop_x: props.stop_x,
      stop_z: props.stop_z,
      tile_x: props.tile_x,
      tile_z: props.tile_z,
      angle: props.angle,
      angle_deg: props.angle_deg,
      speed: props.speed,
      forward_step: props.forward_step,
      direction: props.direction,
      intersection_arrival: props.intersection_arrival,
      patience: props.patience,
      step_count: props.step_count,
      lookahead: props.lookahead,
      states: props.states,
      exists: props.exists,
      color: props.color,
      turn_choice: props.turn_choice,
      signal_choice: props.signal_choice,
      lights: props.lights,
      bbox_w: props.bbox_w,
      bbox_l: props.bbox_l,
      socket: props.socket,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ 
      agent_id: nextProps.agent_id,
      id: nextProps.id,
      pos_x: nextProps.pos_x,
      pos_z: nextProps.pos_z,
      prev_pos_x: nextProps.prev_pos_x,
      prev_pos_z: nextProps.prev_pos_z,
      stop_x: nextProps.stop_x,
      stop_z: nextProps.stop_z,
      tile_x: nextProps.tile_x,
      tile_z: nextProps.tile_z,
      angle: nextProps.angle,
      angle_deg: nextProps.angle_deg,
      speed: nextProps.speed,
      forward_step: nextProps.forward_step,
      direction: nextProps.direction,
      intersection_arrival: nextProps.intersection_arrival,
      patience: nextProps.patience,
      step_count: nextProps.step_count,
      lookahead: nextProps.lookahead,
      states: nextProps.states,
      exists: nextProps.exists,
      color: nextProps.color,
      turn_choice: nextProps.turn_choice,
      signal_choice: nextProps.signal_choice,
      lights: nextProps.lights,
      bbox_w: nextProps.bbox_w,
      bbox_l: nextProps.bbox_l,
      socket: nextProps.socket,
    });
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    return (
            <div>
                {/* Render a Dial */}
                <AngleDial  angle_deg={this.state.angle_deg} 
                            agent_id={this.state.agent_id} 
                            agent_color={this.state.color} 
                            angle_pass={this.angle_pass} 
                            socket={this.state.socket} 
                            update_from_sim={this.props.update_from_sim}/>

                  {/* Render Agent Information */}
     
                {/*<LightDrop  agent_id={this.state.agent_id} 
                            lights={this.state.lights}
                            lights_pass={this.lights_pass}
                            socket={this.state.socket} /> */}
                <AgentInfo    agent_id={this.state.agent_id}
                              id={this.state.agent_id}
                              pos_x={this.state.pos_x}
                              pos_z={this.state.pos_z}
                              prev_pos_x={this.state.prev_pos_x}
                              prev_pos_z={this.state.prev_pos_z}
                              stop_x={this.state.stop_x}
                              stop_z={this.state.stop_z}
                              tile_x={this.state.tile_x}
                              tile_z={this.state.tile_z}
                              angle={this.state.angle}
                              angle_deg={this.state.angle_deg}
                              speed={this.state.speed}
                              forward_step={this.state.forward_step}
                              direction={this.state.direction}
                              intersection_arrival={this.state.intersection_arrival}
                              patience={this.state.patience}
                              step_count={this.state.step_count}
                              lookahead={this.state.lookahead}
                              states={this.state.states}
                              exists={this.state.exists}
                              color={this.state.color} 
                              turn_choice={this.state.turn_choice} 
                              signal_choice={this.state.signal_choice} 
                              lights={this.state.lights} 
                              bbox_w={this.state.bbox_w} 
                              bbox_l={this.state.bbox_l} />
                <TurnChoice  agent_id={this.state.agent_id} 
                             turn_choice={this.state.turn_choice}
                             socket={this.state.socket} />
                <SignalChoice   agent_id={this.state.agent_id} 
                                signal_choice={this.state.signal_choice}
                                socket={this.state.socket} />
                <ForwardStep forward_step={this.state.forward_step} 
                             agent_id={this.state.agent_id} 
                             agent_color={this.state.color} 
                             socket={this.state.socket} />
                <BoundingBox width={this.state.bbox_w} 
                             length={this.state.bbox_l} 
                             agent_id={this.state.agent_id} 
                             agent_color={this.state.color} 
                             socket={this.state.socket} />
                <DeleteAgent  agent_id={this.state.agent_id}
                              socket={this.state.socket} />
             </div>
          );
    }
}

// Allow it to be called in other functions
export default Agent;
