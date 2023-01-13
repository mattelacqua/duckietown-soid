// Import React
import React from "react";

// Import Basic Knob from react-dial-kknob
//import { Basic } from "react-dial-knob";
import CircularSlider from '@fseehawer/react-circular-slider'

// Component for AngleDial (rendered from Agent)
class AngleDial extends React.Component {

  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    this.state = {
      value: props.angle_deg, // Value of the the angle is
      last_sent: props.angle_deg, // Value of the the angle is
      id: props.agent_id,     // Which agent
      color: props.agent_color,     // Which agent
      socket: props.socket,     // Socket
    };
    this.tick = this.tick.bind(this);
  }

  // Update the dial state on new changes 
  handleChange = (newValue) => {
    this.setState({value: newValue});
  };

  // Emit tick
  tick(){
      if (this.state.value !== this.state.last_sent) {
        this.state.socket.emit('agent_angle',
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


  // Render the Dial component from the react-dial-knob package
  render() {
    const color = this.props.agent_color
    return (
      <div>
        <p> Angle Dial </p>
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
            knobPosition="right"
            direction={-1}
            dataIndex={this.props.angle_deg}
            onChange={value => {this.handleChange(value)}}
        />
      </div>
    )
    } // End Render
} // End Class

// Let us use in other componenets
export default AngleDial;
