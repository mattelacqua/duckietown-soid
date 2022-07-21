import React from "react";


// Component to spit out agent information
class AgentInfo extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      agent_id: props.agent_id,
      cur_angle: props.cur_angle,
      cur_pos: props.cur_pos,
      color: props.color,
      lights: props.lights,
    };
  }

  // Render the information to screen
  render() {
    const color = this.props.color
    return (
      <div style={{
            color: color,
      }}>
          {/* HTML FOR ALL THE INFORMATION */}
          <h1> Agent: {this.props.agent_id} </h1>
          <h1> Current Angle: {this.props.cur_angle} </h1>
          <h1> Current Pos: {this.props.cur_pos} </h1>
          <h1> Color: {this.props.color} </h1>
          <h1> {JSON.stringify(this.props.lights)} </h1>
      </div>
      );
    }
}


export default AgentInfo;
