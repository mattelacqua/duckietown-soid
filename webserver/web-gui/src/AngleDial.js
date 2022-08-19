// Import React
import React from "react";

// Import Basic Knob from react-dial-kknob
//import { Basic } from "react-dial-knob";
import CircularSlider from '@fseehawer/react-circular-slider'
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
      last_sent: props.cur_angle, // Value of the the angle is
      id: props.agent_id,     // Which agent
      color: props.agent_color,     // Which agent
    };
    this.tick = this.tick.bind(this);
  }

  // Update the dial state on new changes 
  handleChange = (newValue) => {
    this.setState({value: newValue});
    this.props.angle_pass(newValue);
    
  };

  // Emit tick
  tick(){
    if (this.state.value !== this.state.last_sent) {
      socket.emit('agent_angle',
                  {
                      'id':this.state.id,         // Pass the agent_id stored in state
                      'value':this.state.value    // Pass the cur_angle stored in state
                  }); // End emit
      this.setState({last_sent: this.state.value});
      }

  }

  componentDidMount() {
    this.interval = setInterval(() => this.tick(), 2000);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      value: nextProps.cur_angle, // Value of the the angle is
      last_sent: nextProps.cur_angle, // Value of the the angle is
      id: nextProps.agent_id,     // Which agent
      color: nextProps.agent_color,     // Which agent
    });
    this.forceUpdate();
  }

  // Render the Dial component from the react-dial-knob package
  render() {
    const color = this.props.agent_color
    return (
        <CircularSlider
            label={this.props.agent_id}
            labelColor={color}
            labelBottom={true}
            knobColor={color}
            progressColorFrom="#eeeeee"
            progressColorTo="#eeeeee"
            progressSize={10}
            trackColor="#eeeeee"
            trackSize={10}
            min={0}
            max={360}
            width={150}
            direction={-1}
            knobPosition="right"
            dataIndex={this.props.cur_angle}
            onChange={value => {this.handleChange(value)}}
        />
    )
    } // End Render
} // End Class

// Let us use in other componenets
export default AngleDial;
