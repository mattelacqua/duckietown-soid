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
    };
  }

  // Render the information to screen
  render() {
    return (
      <div>
          {/* HTML FOR ALL THE INFORMATION */}
          <p> Agent: {this.state.agent_id} </p>
          <p> Current Angle: {this.state.cur_angle} </p>
          <p> Current Pos: {this.state.cur_pos} </p>
          <p> Color: {this.state.color} </p>
      </div>
      );
    }
}


export default AgentInfo;
