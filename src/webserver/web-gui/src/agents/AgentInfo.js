import React from "react";

import ReactTextCollapse from 'react-text-collapse';


// Component to spit out agent information
class AgentInfo extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  // Render the information to screen
  render() {
    const color = this.props.agent.color;
    const collapse_options = {
        collapse: true,
        collapseText: '<----------- show more ----------->',
        expandText: '----------> show less <-----------',
        minHeight: 100,
        maxHeight: 400,
        display: 'float',
        textStyle: {
          color: color,
          padding: '10px',
          fontWeight: 'normal',
        },
      };

    let agent = this.props.agent;
    return (
      <div>
        <ReactTextCollapse
          options={collapse_options}>
            <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
      
            {"\n"} {agent.agent_id} General Info: {"\n"}
              &nbsp;&nbsp; color: <span style={{float:'right', 'margin-right': '20px'}}> {agent.color} </span> {"\n"}
              &nbsp;&nbsp; step_count: <span style={{float:'right', 'margin-right': '20px'}}> {agent.step_count} </span> {"\n"}

            {"\n"} {agent.agent_id} Pose: {"\n"}
              &nbsp;&nbsp; pos_x. <span style={{float:'right', 'margin-right': '20px'}}> {agent.pos_x} </span> {"\n"}
              &nbsp;&nbsp; pos_y. <span style={{float:'right', 'margin-right': '20px'}}> {agent.pos_z} </span> {"\n"}
              &nbsp;&nbsp; prev_pos_x. <span style={{float:'right', 'margin-right': '20px'}}> {agent.prev_pos_x} </span> {"\n"}
              &nbsp;&nbsp; prev_pos_y. <span style={{float:'right', 'margin-right': '20px'}}> {agent.prev_pos_z} </span> {"\n"}
              &nbsp;&nbsp; stop_x. <span style={{float:'right', 'margin-right': '20px'}}> {agent.stop_x} </span> {"\n"}
              &nbsp;&nbsp; stop_y. <span style={{float:'right', 'margin-right': '20px'}}> {agent.stop_z} </span> {"\n"}
              &nbsp;&nbsp; tile_x. <span style={{float:'right', 'margin-right': '20px'}}> {agent.tile_x} </span> {"\n"}
              &nbsp;&nbsp; tile_y. <span style={{float:'right', 'margin-right': '20px'}}> {agent.tile_y} </span> {"\n"}
              &nbsp;&nbsp; angle. <span style={{float:'right', 'margin-right': '20px'}}> {agent.angle} </span> {"\n"}
              &nbsp;&nbsp; angle_deg. <span style={{float:'right', 'margin-right': '20px'}}> {agent.angle_deg} </span> {"\n"}
              &nbsp;&nbsp; current_direction. <span style={{float:'right', 'margin-right': '20px'}}> {agent.direction} </span> {"\n"}
              &nbsp;&nbsp; initial_direction. <span style={{float:'right', 'margin-right': '20px'}}> {agent.initial_direction} </span> {"\n"}

            {"\n"} {agent.agent_id} State: {"\n"}
              &nbsp;&nbsp; speed. <span style={{float:'right', 'margin-right': '20px'}}> {agent.speed} </span> {"\n"}
              &nbsp;&nbsp; forward_step. <span style={{float:'right', 'margin-right': '20px'}}> {agent.forward_step} </span> {"\n"}
              &nbsp;&nbsp; patience. <span style={{float:'right', 'margin-right': '20px'}}> {agent.patience} </span> {"\n"}
              &nbsp;&nbsp; intersection_arrival. <span style={{float:'right', 'margin-right': '20px'}}> {agent.intersection_arrival} </span> {"\n"}
              &nbsp;&nbsp; turn_choice. <span style={{float:'right', 'margin-right': '20px'}}> {agent.turn_choice} </span> {"\n"}
              &nbsp;&nbsp; signal_choice. <span style={{float:'right', 'margin-right': '20px'}}> {agent.signal_choice} </span> {"\n"}
              &nbsp;&nbsp; lookahead. <span style={{float:'right', 'margin-right': '20px'}}> {agent.lookahead} </span> {"\n"}
              &nbsp;&nbsp; bbox_w. <span style={{float:'right', 'margin-right': '20px'}}> {agent.bbox_w} </span> {"\n"}
              &nbsp;&nbsp; bbox_l. <span style={{float:'right', 'margin-right': '20px'}}> {agent.bbox_l} </span> {"\n"}
              &nbsp;&nbsp; in_intersection. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.in_intersection.toString()} </span> {"\n"}
              &nbsp;&nbsp; at_intersection_entry. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.at_intersection_entry.toString()} </span> {"\n"}
              &nbsp;&nbsp; intersection_empty. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.intersection_empty.toString()} </span> {"\n"}
              &nbsp;&nbsp; approaching_intersection. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.approaching_intersection.toString()} </span> {"\n"}
              &nbsp;&nbsp; obj_in_range. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.obj_in_range.toString()} </span> {"\n"}
              &nbsp;&nbsp; has_right_of_way. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.has_right_of_way.toString()} </span> {"\n"}
              &nbsp;&nbsp; next_to_go. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.next_to_go.toString()} </span> {"\n"}
              &nbsp;&nbsp; safe_to_enter. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.safe_to_enter.toString()} </span> {"\n"}
              &nbsp;&nbsp; cars_waiting_to_enter. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.cars_waiting_to_enter.toString()} </span> {"\n"}
              &nbsp;&nbsp; car_entering_range. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.car_entering_range.toString()} </span> {"\n"}
              &nbsp;&nbsp; obj_behind_intersection. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.obj_behind_intersection.toString()} </span> {"\n"}
              &nbsp;&nbsp; is_tailgating. <span style={{float:'right', 'margin-right': '20px'}}> {agent.state.is_tailgating.toString()} </span> {"\n"}
            </p>
        </ReactTextCollapse>
      </div>
    );
  }
}

export default AgentInfo;
