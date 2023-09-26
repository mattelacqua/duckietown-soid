// Import React
import React from "react";

// Import the circular slider
import CircularSlider from '@fseehawer/react-circular-slider'
import './AngleDial.css'

// Component for AngleDial (rendered from Agent)
class AngleDial extends React.Component {

  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    this.state = {
      value: 0, // Value of the the angle is
      last_sent: 0, // Value of the the angle is
    };
    this.tick = this.tick.bind(this);
  }

  // Once the component mounts
  componentDidMount() {
    this.interval = setInterval(() => this.tick(), 2000);
  }

  // Update the dial state on new changes 
  handleChange = (newValue) => {
    this.setState({value: newValue});
  };

  // This is called every 2 seconds
  tick(){
    // If we have a new value
    if (this.state.value !== this.state.last_sent) {
      this.props.socket.emit(
        'agent_angle',
        {
            'id':this.props.agent.id,         
            'value':this.state.value,    
        }); // End emit
    }
    this.setState({last_sent: this.state.value}); 
  }

  // Render the Dial component from the react-dial-knob package
  render() {
    return (
      <CircularSlider
        progressColorFrom="#eeeeee"
        progressColorTo="#eeeeee"
        progressSize={10}
        trackColor="#eeeeee"
        trackSize={10}
        min={0}
        max={360}
        width={150}
        knobPosition="left"
        direction={-1}
        dataIndex={this.props.agent.angle_deg}
        onChange={value => {this.handleChange(value)}}
      />
    )
  } // End Render
} // End Class

// Let us use in other componenets
export default AngleDial;
