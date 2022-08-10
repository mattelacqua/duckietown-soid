// Import React
import React from "react";

// Import Angle Dial 
import AngleDial from './AngleDial.js'

// Import Agent Info Screen
import AgentInfo from './AgentInfo.js'

// Import Agent Info Screen
import LightDrop from './LightDrop.js'

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
      lights: props.lights
    };
    this.angle_pass = this.angle_pass.bind(this); // Bind angle pass to this component
    this.lights_pass = this.lights_pass.bind(this); // Bind angle pass to this component
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ 
      agent_id: nextProps.agent_id,
      cur_pos: nextProps.cur_pos,
      cur_angle: nextProps.cur_angle,
      color: nextProps.color,
      lights: nextProps.light
    });
  }

  // Handler to pass to child to update the state of the agent, which forces a
  // re-render. We call this in AgentDial when we update the dial so the text updates as well.
  angle_pass(angle) {
    this.setState({
        cur_angle: angle
    });
  }


  // Pass the light change into agent state
  lights_pass(newLight) {
    const old_lights = this.state.lights;
    const new_lights = [newLight];
    const updated = old_lights.map(obj => new_lights.find(o => o.light === obj.light) || obj);
    this.setState({
        lights: updated
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
                            angle_pass={this.angle_pass} />

                  {/* Render Agent Information */}
                <AgentInfo    agent_id={this.state.agent_id}
                              cur_angle={this.state.cur_angle}
                              cur_pos= {this.state.cur_pos}
                              color={this.state.color} 
                              lights={this.state.lights}/>
      
                <LightDrop  agent_id={this.state.agent_id} 
                            lights={this.state.lights}
                            lights_pass={this.lights_pass}/>
              </div>
          );
    }
}

// Allow it to be called in other functions
export default Agent;
