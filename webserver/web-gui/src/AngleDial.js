// Import React
import React from "react";

// Import Basic Knob from react-dial-kknob
import { Basic } from "react-dial-knob";

// Import io from socket to send to backend flask
import io from 'socket.io-client';

// Create the socket
const socket = io();

// Component for AngleDial (rendered from Agent)
class AngleDial extends React.Component {

  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    this.state = {
      value: props.cur_angle, // Value of the the angle is
      id: props.agent_id,     // Which agent
      color: props.agent_color,     // Which agent
    };
  }

  // Update the dial state on new changes
  handleChange = (newValue) => {
    this.setState({value: newValue});
    this.props.angle_pass(newValue);
    socket.emit('agent_angle',
                {
                    'id':this.state.id,         // Pass the agent_id stored in state
                    'value':this.state.value    // Pass the cur_angle stored in state
                }); // End emit

  };
  

  // Render the Dial component from the react-dial-knob package
  render() {
    const color = this.state.color
    return (<Basic
          diameter={200}
          min={0}
          max={360}
          step={1}
          value={this.state.value} // Set its value to the state value
          theme={{
              defaultColor: '#333',
              activeColor: color,
          }}
          style={{
            position: 'relative',
            margin: '100px auto',
            width: '200px',
          }}
          onValueChange={this.handleChange} // When the value gets changed, call our handleChange method
          ariaLabelledBy={'my-label'} // Label beneath it
          spaceMaxFromZero={false}
        > 
          <label id={'my-label'} style={{
            textAlign: 'center',
            width: '200px',
            display: 'block',
            padding: '10px 0'
          }}>Agent: {this.state.id}</label>
      </Basic> );
    } // End Render
} // End Class

// Let us use in other componenets
export default AngleDial;
