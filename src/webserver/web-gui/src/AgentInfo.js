import React from "react";

import ReactTextCollapse from 'react-text-collapse';


// Component to spit out agent information
class AgentInfo extends React.Component {

  // Construct so it takes properties and they are information
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
    };
  }

  componentWillReceiveProps(nextProps){
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
      
                  agent: {this.props.agent_id} {"\n"}
                  pos_x: {this.props.pos_x} {"\n"}
                  pos_z: {this.props.pos_z} {"\n"}
                  prev_pos_x: {this.props.prev_pos_x} {"\n"}
                  prev_pos_z: {this.props.prev_pos_z} {"\n"}
                  stop_x: {this.props.stop_x} {"\n"}
                  stop_z: {this.props.stop_z} {"\n"}
                  tile_x: {this.props.tile_x} {"\n"}
                  tile_z: {this.props.tile_z} {"\n"}
                  angle: {this.props.angle} {"\n"}
                  angle_deg: {this.props.angle_deg} {"\n"}
                  speed: {this.props.speed} {"\n"}
                  forward_step: {this.props.forward_step} {"\n"}
                  direction: {this.props.direction} {"\n"}
                  intersection_arrival: {this.props.intersection_arrival} {"\n"}
                  patience: {this.props.patience} {"\n"}
                  step_count: {this.props.step_count} {"\n"}
                  lookahead: {this.props.lookahead} {"\n"}
                  exists: {this.props.exists} {"\n"}
                  color: {this.props.color} {"\n"}
                  turn_choice: {this.props.turn_choice} {"\n"}
                  signal_choice: {this.props.signal_choice} {"\n"}
                  bbox_w: {this.props.bbox_w} {"\n"}
                  bbox_l: {this.props.bbox_l} {"\n"}
                  {"\n"} Agent State: {"\n"}
                  in_intersection: {this.props.states.in_intersection.toString()} {"\n"}
                  at_intersection_entry: {this.props.states.at_intersection_entry.toString()} {"\n"}
                  intersection_empty: {this.props.states.intersection_empty.toString()} {"\n"}
                  approaching_intersection: {this.props.states.approaching_intersection.toString()} {"\n"}
                  obj_in_range: {this.props.states.obj_in_range.toString()} {"\n"}
                  has_right_of_way: {this.props.states.has_right_of_way.toString()} {"\n"}
                  cars_waiting_to_enter: {this.props.states.cars_waiting_to_enter.toString()} {"\n"}
                  car_entering_range: {this.props.states.car_entering_range.toString()} {"\n"}
                  obj_behind_intersection: {this.props.states.obj_behind_intersection.toString()} {"\n"}
                  is_tailgating: {this.props.states.is_tailgating.toString()} {"\n"}
                  next_to_go: {this.props.states.next_to_go.toString()} {"\n"}
                  {"\n"} Agent Lights: {"\n"}
                  front_right: {this.props.lights.front_right[3].toString()} {"\n"}
                  front_left: {this.props.lights.front_left[3].toString()} {"\n"}
                  center: {this.props.lights.center[3].toString()} {"\n"}
                  back_right: {this.props.lights.back_right[3].toString()} {"\n"}
                  back_left: {this.props.lights.back_left[3].toString()} {"\n"}
                  </p>
        </ReactTextCollapse>
      </div>
      );
    }
}


export default AgentInfo;
