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
      
            {"\n"} {agent.agent_id} Info: {"\n"}
            index: {agent.index} {"\n"}
            color: {agent.color} {"\n"}
            exists: {agent.exists} {"\n"}
            step_count: {agent.step_count} {"\n"}

            {"\n"} Agent Pose: {"\n"}
            pos_x: {agent.pos_x} {"\n"}
            pos_z: {agent.pos_z} {"\n"}
            prev_pos_x: {agent.prev_pos_x} {"\n"}
            prev_pos_z: {agent.prev_pos_z} {"\n"}
            stop_x: {agent.stop_x} {"\n"}
            stop_z: {agent.stop_z} {"\n"}
            tile_x: {agent.tile_x} {"\n"}
            tile_z: {agent.tile_z} {"\n"}
            angle: {agent.angle} {"\n"}
            angle_deg: {agent.angle_deg} {"\n"}
            current_direction: {agent.direction} {"\n"}
            initial_direction: {agent.initial_direction} {"\n"}

            {"\n"} Agent State: {"\n"}
            speed: {agent.speed} {"\n"}
            forward_step: {agent.forward_step} {"\n"}
            patience: {agent.patience} {"\n"}
            intersection_arrival: {agent.intersection_arrival} {"\n"}
            turn_choice: {agent.turn_choice} {"\n"}
            signal_choice: {agent.signal_choice} {"\n"}
            lookahead: {agent.lookahead} {"\n"}
            bbox_w: {agent.bbox_w} {"\n"}
            bbox_l: {agent.bbox_l} {"\n"}

            {"\n"} Agent State: {"\n"}
            in_intersection: {agent.state.in_intersection.toString()} {"\n"}
            at_intersection_entry: {agent.state.at_intersection_entry.toString()} {"\n"}
            intersection_empty: {agent.state.intersection_empty.toString()} {"\n"}
            approaching_intersection: {agent.state.approaching_intersection.toString()} {"\n"}
            obj_in_range: {agent.state.obj_in_range.toString()} {"\n"}
            has_right_of_way: {agent.state.has_right_of_way.toString()} {"\n"}
            next_to_go: {agent.state.next_to_go.toString()} {"\n"}
            safe_to_enter: {agent.state.safe_to_enter.toString()} {"\n"}
            cars_waiting_to_enter: {agent.state.cars_waiting_to_enter.toString()} {"\n"}
            car_entering_range: {agent.state.car_entering_range.toString()} {"\n"}
            obj_behind_intersection: {agent.state.obj_behind_intersection.toString()} {"\n"}
            is_tailgating: {agent.state.is_tailgating.toString()} {"\n"}
            </p>
        </ReactTextCollapse>
      </div>
    );
  }
}

export default AgentInfo;
