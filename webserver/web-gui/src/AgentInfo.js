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
            textAlign: 'left',
            whiteSpace: 'pre-line',
      }}>
          {/* HTML FOR ALL THE INFORMATION */}
          <p> Agent: {this.props.agent_id} {"\n"}
              Current Angle: {this.props.cur_angle} {"\n"}
              Current Pos: {JSON.stringify(this.props.cur_pos)} {"\n"}
              Color: {this.props.color} {"\n"}
              {JSON.stringify(this.props.lights)} </p>
      </div>
      );
    }
}


export default AgentInfo;
