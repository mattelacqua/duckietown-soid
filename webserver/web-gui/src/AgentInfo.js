import React from "react";

import ReactTextCollapse from 'react-text-collapse';


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
      turn_choice: props.turn_choice,
      signal_choice: props.signal_choice,
      forward_step: props.forward_step,
      bbox_w: props.bbox_w,
      bbox_l: props.bbox_l,
    };
  }

  componentWillReceiveProps(nextProps){
    this.setState({
      agent_id: nextProps.agent_id,
      cur_angle: nextProps.cur_angle,
      cur_pos: nextProps.cur_pos,
      color: nextProps.color,
      lights: nextProps.lights,
      signal_choice: nextProps.signal_choice,
      forward_step: nextProps.forward_step,
      bbox_w: nextProps.bbox_w,
      bbox_l: nextProps.bbox_l,
    });
  }

  // Render the information to screen
  render() {
    const color = this.props.color
    const collapse_options = {
        collapse: true,
        collapseText: '<--- show more --->',
        expandText: '--> show less <---',
        minHeight: 50,
        maxHeight: 150,
        textStyle: {
          color: color,
          padding: '10px',
          fontWeight: 'normal',
        },
      }

    return (
      <div>
        <ReactTextCollapse
          options={collapse_options}>
              {/* HTML FOR ALL THE INFORMATION */}
              <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
                }}> 
      
                  Agent: {this.props.agent_id} {"\n"}
                  Current Angle: {this.props.cur_angle} {"\n"}
                  Current Pos: {JSON.stringify(this.props.cur_pos)} {"\n"}
                  Color: {this.props.color} {"\n"}
                  Turn Choice: {this.props.turn_choice} {"\n"}
                  Signal Choice: {this.props.signal_choice} {"\n"}
                  Forward Step: {this.props.forward_step} {"\n"}
                  Bounding Box Offset Width: {this.props.bbox_w} {"\n"}
                  Bounding Box Offset Length: {this.props.bbox_l} {"\n"}
                  </p>
        </ReactTextCollapse>
      </div>
      );
    }
}


export default AgentInfo;
