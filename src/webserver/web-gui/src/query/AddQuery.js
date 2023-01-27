// Import React
import React from "react";

import QueryType from "./QueryType.js";
import SingleDirection from "./SingleDirection.js";
import MultiDirection from "./MultiDirection.js";
import QueryRange from "./QueryRange.js";

import ValueType from "./ValueType.js";

// Agent Component (gets rendered in app)
class AddQuery extends React.Component {

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
        is_gt: false,
        is_lt: false,
        is_gte: false,
        is_lte: false,
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
    this.set_operator = this.set_operator.bind(this); // Bind this to update_from sim 
    this.handleClick = this.handleClick.bind(this); // Bind this to update_from sim 
  }

  // Callback function for query_type to set our state function
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

    // Callback function for query_type to set our state function
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
    }
    
    // Callback function for seting mutliple directions
    set_multi_direction(directions){
      this.setState({
        range: {
          is_gt: false,
          is_lt: false,
          is_gte: false,
          is_lte: false,
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

    // Callback function for setting the operartor
    set_operator(operator){
      var range = {...this.state.range}
      if (operator === '>'){
        range.is_gt = true;
        range.is_lt = false;
        range.is_gte = false;
        range.is_lte = false;
      }
      if (operator === '<'){
        range.is_gt = false;
        range.is_lt = true;
        range.is_gte = false;
        range.is_lte = false;
      }     
      if (operator === '>='){
        range.is_gt = false;
        range.is_lt = false;
        range.is_gte = true;
        range.is_lte = false;
      }     
      if (operator === '<='){
        range.is_gt = false;
        range.is_lt = false;
        range.is_gte = false;
        range.is_lte = true;
      }     
      this.setState({range});
    }    
  
  handleClick(){
    this.props.socket.emit(
      "add_counterfactual",
      {
        index: this.props.agent.id,
        counterfactual: this.state,
      }
    )
  }
  handleKeyPress(){
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
    let input_value;
    if (this.state.is_value){
      // x position value
      if (this.state.is_pos_x) {
        console.log("Agent", this.props.agent.pos_x);
        input_value =  
          <form>
            <label>
              Agent x position:   
              <input type="text" 
                    value={this.state.value}
                    onChange = {(e) => {
                      console.log("change value", e);
                      this.setState({
                        value: e.target.value,
                      });
                    }
                    }
              />
            </label>  
          </form>
      }
      // Z position value
      if (this.state.is_pos_z) {
        input_value =  
          <form>
            <label>
              Agent z position:   
              <input type="text" 
                    value={this.state.value}
                    onChange = {(e) => {
                      console.log("change value", e);
                      this.setState({
                        value: e.target.value,
                      });
                    }
                    }
              />
            </label>  
          </form>
      }    
      // Angle Value
      if (this.state.is_angle) {
        input_value =  
          <form>
            <label>
              Agent angle:   
              <input type="text" 
                    value={this.state.value}
                    onChange = {(e) => {
                      console.log("change value", e);
                      this.setState({
                        value: e.target.value,
                      });
                    }
                    }
              />
            </label>  
          </form>
      }       
      // Forward Step Value
      if (this.state.is_forward_step) {
        input_value =  
          <form>
            <label>
              Agent forward_step:   
              <input type="text" 
                    value={this.state.value}
                    onChange = {(e) => {
                      console.log("change value", e);
                      this.setState({
                        value: e.target.value,
                      });
                    }
                    }
              />
            </label>  
          </form>
      }       
      // Speed Value
      if (this.state.is_speed) {
        input_value =  
          <form>
            <label>
              Agent z position:   
              <input type="text" 
                    value={this.state.value}
                    onChange = {(e) => {
                      console.log("change value", e);
                      this.setState({
                        value: e.target.value,
                      });
                    }
                    }
              />
            </label>  
          </form>
      }    
      // Signal Choice 
      if (this.state.is_signalchoice) {
        input_value =  
          <SingleDirection  direction={this.props.agent.signal_choice}
                            set_single_direction={this.set_single_direction}
                            signal_or_turn="Signal"
          />
      }
      // Signal Choice 
      if (this.state.is_turnchoice) {
        input_value =  
          <SingleDirection  direction={this.props.agent.turn_choice}
                            set_single_direction={this.set_single_direction}
                            signal_or_turn="Turn"
          />
      }
    };
    if (this.state.is_range){
      // x position value
      if (this.state.is_pos_x) {
        input_value =  
          <QueryRange default_val={this.props.agent.pos_x}
                        set_bound={this.set_bound}
                        set_operator={this.set_operator}
          />
      }
      // Z position value
      if (this.state.is_pos_z) {
        input_value =
          <QueryRange default_val={this.props.agent.pos_z}
                      set_bound={this.set_bound}
                      set_operator={this.set_operator}
          />
      }    
      // Angle Value
      if (this.state.is_angle) {
        input_value =  
          <QueryRange default_val={this.props.agent.angle}
                      set_bound={this.set_bound}
                      set_operator={this.set_operator}
        />
      }       
      // Forward Step Value
      if (this.state.is_forward_step) {
        input_value =  
          <QueryRange default_val={this.props.agent.forward_step}
                      set_bound={this.set_bound}
                      set_operator={this.set_operator}
          />
      }       
      // Speed Value
      if (this.state.is_speed) {
        input_value =  
          <QueryRange  default_val={this.props.agent.forward_step}
                       set_bound={this.set_bound}
                       set_operator={this.set_operator}
          />
      }    
      // Signal Choice 
      if (this.state.is_signalchoice) {
        input_value =  
          <MultiDirection direction={this.props.agent.signal_choice}
                          set_multi_direction={this.set_single_direction}
          />
      }
      // Signal Choice 
      if (this.state.is_turnchoice) {
        input_value =  
          <MultiDirection  direction={this.props.agent.turn_choice}
                           set_multi_direction={this.set_single_direction}
          />
      }
    }

    return (
            <div>
                {/* Render */}
                <QueryType  is_pos_x={this.state.is_pos_x}
                            is_pos_z={this.state.is_pos_z}
                            is_angle={this.state.is_angle}
                            is_forward_step={this.state.is_forward_step}
                            is_speed={this.state.is_speed}
                            is_signalchoice={this.state.is_signalchoice}
                            is_turnchoice={this.state.is_turnchoice}
                            set_type={this.set_type}
                />
                <ValueType  is_value={this.state.is_value}
                            is_range={this.state.is_range}
                            set_value_type={this.set_value_type}
                />
                {input_value}
                <button onClick= {this.handleClick}> Add Query  </button>
             </div>
          );
    }
}

// Allow it to be called in other functions
export default AddQuery;
