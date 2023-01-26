// Import React
import React from "react";

import QueryType from "./QueryType.js";


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
    console.log(this.state);
  }


  // Render the agent component 
  render() {

    // There may be several renders here based on conditionals on the state, and what values of state are true.
    // You may have to build more components as well like 'text boxes' or call out to Angle Dial or things like that.
    // I can do some of that or help you learn how. Just reach out and lmk
    // Will end with a button to add the query.
    // Imagine Dropdown for proposition (pos_x, angle, signal, etc), dropdown for is_value / is_range, depending on that, text input box or 2 text input boxes with a operator drop down between
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
             </div>
          );
    }
}

// Allow it to be called in other functions
export default AddQuery;
