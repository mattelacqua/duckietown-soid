// Import React
import React from "react";

// Import Range 
import InputRange from 'react-input-range';
import "react-input-range/lib/css/index.css";

import "./ForwardStep.css";

// Component for AngleDial (rendered from Agent)
class BoundingBox extends React.Component {

  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    this.state = {
      width: this.props.width,
      length: this.props.length,
      color: props.agent_color,
      id: props.agent_id,     // Which agent
      socket: props.socket,     // Socket
    };
  }

  // Update the dial state on new changes 
  handleChange = (newValue, direction) => {
    this.state.socket.emit('bounding_box',
                    {
                        'id':this.state.id,         // Pass the agent_id stored in state
                        'bbox_offset':newValue,    // Pass the new offset
                        'direction':direction,    // Pass the cur_angle stored in state
                    }); // End emit
     this.setState({direction: newValue}); 
  };

  // Render the Dial component from the react-dial-knob package
  render() {
    const color = this.props.agent_color
    return (
      <div>
      <div>
        <form classname="form">
        <p> Variance in Bounding Box Width </p> 
          <InputRange
              maxValue = {1}
              minValue = {0}
              value={this.state.width}
              step = {0.01}
              onChangeComplete={value => {this.handleChange(value, "width")}}
              onChange={value => this.setState({ width:value })}
          />
        </form>
      </div>
      <div>
      <form classname="form">
        <p> Variance in Bounding Box Length </p>
          <InputRange
              maxValue = {1}
              minValue = {0}
              value={this.state.length}
              step = {0.01}
              onChangeComplete={value => {this.handleChange(value, "length")}}
              onChange={value => this.setState({ length:value })}
          />
        </form>
      </div>
      </div>

    )
    } // End Render
} // End Class

// Let us use in other componenets
export default BoundingBox;
