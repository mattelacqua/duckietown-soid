// Import React
import React from "react";

// Import Range 
import InputRange from 'react-input-range';
import "react-input-range/lib/css/index.css";

import "./ForwardStep.css";

// Component for AngleDial (rendered from Agent)
class ForwardStep extends React.Component {

  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    this.state = {
      value: {
            min: props.forward_step,
            max: props.forward_step,
        },
      color: props.agent_color,
      id: props.agent_id,     // Which agent
      socket: props.socket,     // Socket
    };
  }

  // Update the dial state on new changes 
  handleChange = (newValue) => {
    this.state.socket.emit('forward_step',
                    {
                        'id':this.state.id,         // Pass the agent_id stored in state
                        'forward_step':newValue    // Pass the cur_angle stored in state
                    }); // End emit
     this.setState({value: newValue}); 
  };

  // Render the Dial component from the react-dial-knob package
  render() {
    const color = this.props.agent_color
    return (
      <form classname="form">
        <p> Forward Step (acceleration) </p>
        <InputRange
            maxValue = {1}
            minValue = {0}
            allowSameValues
            value={this.state.value}
            step = {0.01}
            ariaLabeledby = {"Forward Step (acceleration)"}
            onChangeComplete={value => {this.handleChange(value)}}
            onChange={value => this.setState({ value })}
        />
      </form>
    )
    } // End Render
} // End Class

// Let us use in other componenets
export default ForwardStep;
