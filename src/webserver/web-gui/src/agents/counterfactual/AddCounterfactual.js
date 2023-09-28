// Import React
import React from "react";

import CounterfactualType from "./CounterfactualType.js";
import SingleDirection from "./SingleDirection.js";
import MultiDirection from "./MultiDirection.js";
import CounterfactualRange from "./CounterfactualRange.js";
import CounterfactualValue from "./CounterfactualValue.js";

import ValueType from "./ValueType.js";
import './Counterfactuals.css'
import '../../environment/StateButtons.css'


// Agent Component (gets rendered in app)
class AddCounterfactual extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      is_pos_x: false,
      is_pos_z: false,
      is_angle: false,
      is_forward_step: false,
      is_speed: false,
      is_signalchoice: false,
      is_turnchoice: false,
      is_value: false,
      is_range: false,
      value: 0.0,
      range: {
        turn_choices: [],
        low_bound: 0.0,
        high_bound: 0.0,
      }
    };

    this.set_type = this.set_type.bind(this); // Bind this to update_from sim
    this.set_value_type = this.set_value_type.bind(this); // Bind this to update_from sim
    this.set_single_direction = this.set_single_direction.bind(this); // Bind this to update_from sim
    this.set_multi_direction = this.set_multi_direction.bind(this); // Bind this to update_from sim
    this.set_bound = this.set_bound.bind(this); // Bind this to update_from sim
    this.set_value = this.set_value.bind(this); // Bind this to update_from sim
    this.set_initial_direction = this.set_initial_direction.bind(this); // Bind this to update_from sim
    this.set_intersection_arrival = this.set_intersection_arrival.bind(this); // Bind this to update_from sim
    this.handleClick = this.handleClick.bind(this); // Bind this to update_from sim

    console.log("RENDERED IT");
  }

  // Callback function for Counterfactual_type to set our state function
  set_type(type){
    console.log("Call back got", type);
    //Pos x
    if (type === 'is_pos_x'){
      this.setState({
        is_pos_x: true,
        is_pos_z: false,
        is_angle: false,
        is_forward_step: false,
        is_speed: false,
        is_signalchoice: false,
        is_turnchoice: false,
      });
    }

    //Pos z
    if (type === 'is_pos_z'){
      this.setState({
        is_pos_x: false,
        is_pos_z: true,
        is_angle: false,
        is_forward_step: false,
        is_speed: false,
        is_signalchoice: false,
        is_turnchoice: false,
      });
    }

    // angle
    if (type === 'is_angle'){
      this.setState({
        is_pos_x: false,
        is_pos_z: false,
        is_angle: true,
        is_forward_step: false,
        is_speed: false,
        is_signalchoice: false,
        is_turnchoice: false,
      });
    }

    // forward_step
    if (type === 'is_forward_step'){
      this.setState({
        is_pos_x: false,
        is_pos_z: false,
        is_angle: false,
        is_forward_step: true,
        is_speed: false,
        is_signalchoice: false,
        is_turnchoice: false,
      });
    }

    // speed
    if (type === 'is_speed'){
      this.setState({
        is_pos_x: false,
        is_pos_z: false,
        is_angle: false,
        is_forward_step: false,
        is_speed: true,
        is_signalchoice: false,
        is_turnchoice: false,
      });
    }

    // signal_choice
    if (type === 'is_signalchoice'){
      this.setState({
        is_pos_x: false,
        is_pos_z: false,
        is_angle: false,
        is_forward_step: false,
        is_speed: false,
        is_signalchoice: true,
        is_turnchoice: false,
      });
    }

    // is_turnchoice
    if (type === 'is_turn_choice'){
      this.setState({
        is_pos_x: false,
        is_pos_z: false,
        is_angle: false,
        is_forward_step: false,
        is_speed: false,
        is_signalchoice: false,
        is_turnchoice: true,
      });
    }
  }

    // Callback function for Counterfactual_type to set our state function
    set_value_type(type){
      console.log("Value type call back got", type);
      //Value
      if (type === 'is_value'){
        this.setState({
          is_value: true,
          is_range: false,
        });
      }

      //Range
      if (type === 'is_range'){
        this.setState({
          is_value: false,
          is_range: true,
        });
      }
    }

    // Callback function for setting a single direction to set our state function
    set_single_direction(value){
      this.setState({
        value: value,
      });
      console.log("STATE", this.state);
      console.log("Value", value);
    }

    // Callback function for seting mutliple directions
    set_multi_direction(directions){
      this.setState({
        range: {
          turn_choices: directions,
          low_bound: 0.0,
          high_bound: 0.0,
        }
      });
    }

    // Callback function for setting the boundss
    set_bound(value, bound){
      var range = {...this.state.range}
      if (bound === 'low'){
        range.low_bound = value;
      }
      if (bound === 'high'){
        range.high_bound = value;
      }
      this.setState({range});
    }

    // Callback function for setting the boundss
    set_value(value){
      this.setState({value: value});
    }

    // Callback function for setting the boundss
    set_initial_direction(value){
      this.setState({initial_direction: value});
    }

    // Callback function for setting the boundss
    set_intersection_arrival(value){
      this.setState({intersection_arrival: value});
    }

  handleClick(){
    console.log("THIS STATE", this.state);
    this.props.socket.emit(
      "add_counterfactual",
      {
        index: this.props.agent.id,
        counterfactual: this.state,
      }
    )
  }

  // Render the agent component
  render() {
    let input_component;
    if (this.state.is_value){
      // x position value
      if (this.state.is_pos_x) {
        input_component =
          <CounterfactualValue default_val = {this.props.agent.pos_x}
                               set_value = {this.set_value} />
      }
      // Z position value
      if (this.state.is_pos_z) {
        input_component =
          <CounterfactualValue default_val = {this.props.agent.pos_z}
                               set_value = {this.set_value} />
      }
      // Angle Value
      if (this.state.is_angle) {
        input_component =
          <CounterfactualValue default_val = {this.props.agent.angle_deg}
                               set_value = {this.set_value} />
      }
      // Forward Step Value
      if (this.state.is_forward_step) {
        input_component =
          <CounterfactualValue default_val = {this.props.agent.forward_step}
                               set_value = {this.set_value} />
      }
      // Speed Value
      if (this.state.is_speed) {
        input_component =
          <CounterfactualValue default_val = {this.props.agent.speed}
                               set_value = {this.set_value} />
      }
      // Signal Choice
      if (this.state.is_signalchoice) {
        input_component =
          <SingleDirection  direction={this.props.agent.signal_choice}
                            set_single_direction={this.set_single_direction} />
      }
      // Signal Choice
      if (this.state.is_turnchoice) {
        input_component =
          <SingleDirection  direction={this.props.agent.turn_choice}
                            set_single_direction={this.set_single_direction} />
      }
    };
    if (this.state.is_range){
      // x position value
      if (this.state.is_pos_x) {
        input_component =
          <CounterfactualRange default_val={this.props.agent.pos_x}
                               set_bound={this.set_bound} />
      }
      // Z position value
      if (this.state.is_pos_z) {
        input_component =
          <CounterfactualRange default_val={this.props.agent.pos_z}
                               set_bound={this.set_bound} />
      }
      // Angle Value
      if (this.state.is_angle) {
        input_component =
          <CounterfactualRange default_val={this.props.agent.angle_deg}
                               set_bound={this.set_bound} />
      }
      // Forward Step Value
      if (this.state.is_forward_step) {
        input_component =
          <CounterfactualRange default_val={this.props.agent.forward_step}
                               set_bound={this.set_bound} />
      }
      // Speed Value
      if (this.state.is_speed) {
        input_component =
          <CounterfactualRange  default_val={this.props.agent.forward_step}
                                set_bound={this.set_bound} />
      }
      // Signal Choice
      if (this.state.is_signalchoice) {
        input_component =
          <MultiDirection direction={this.props.agent.signal_choice}
                          set_multi_direction={this.set_multi_direction} />
      }
      // Signal Choice
      if (this.state.is_turnchoice) {
        input_component =
          <MultiDirection  direction={this.props.agent.turn_choice}
                           set_multi_direction={this.set_multi_direction} />
      }
    }

    return (
      <div className="AddCounterfactuals">
        <div className="SpecCounterfactual">
          {/* Render */}
          <p>Suppose</p>
          <CounterfactualType
            is_pos_x={this.state.is_pos_x}
            is_pos_z={this.state.is_pos_z}
            is_angle={this.state.is_angle}
            is_forward_step={this.state.is_forward_step}
            is_speed={this.state.is_speed}
            is_signalchoice={this.state.is_signalchoice}
            is_turnchoice={this.state.is_turnchoice}
            set_type={this.set_type} />
          <p>had</p>
          <ValueType  is_value={this.state.is_value}
                      is_range={this.state.is_range}
                      set_value_type={this.set_value_type} />
        </div>
        <div style={{ visibility: (input_component) ? 'visible' : 'hidden'}}>
          <div className="InnerSpec">
            {(input_component) ? input_component : <CounterfactualValue default_val = {0} set_value = {() => {}} />}
          </div>
        </div>
        <div className="SetCounterfactual">
          <div class='StateButtons'>
            <button className='addcounterfac'onClick= {this.handleClick}> Add Counterfactual  </button>
          </div>
        </div>
      </div>
    );
  }
}

// Allow it to be called in other functions
export default AddCounterfactual;
