// Import React
import React from "react";

// Import Basic Knob from react-dial-kknob
//import { Basic } from "react-dial-knob";
import CircularSlider from '@fseehawer/react-circular-slider'
import App from "./App";

// Component for AngleDial (rendered from Agent)
class AngleDial extends React.Component {

  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    this.state = {
      value: 0, // Value of the the angle is
      last_sent: 0, // Value of the the angle is
      id: props.agent_id,     // Which agent
      color: props.agent_color,     // Which agent
      include_counterfactual: false, // decide if we want to include counterfactual
      socket: props.socket,     // Socket
    };
    this.tick = this.tick.bind(this);
  }

  // Update the dial state on new changes 
  handleChange = (newValue) => {
    this.setState({value: newValue});
  };

  include_counterfactual = (newValue) => {
    this.setState({include_counterfactual: newValue});
  };
  // Emit tick
  tick(){
      if (this.state.value !== this.state.last_sent) {
        this.props.update_from_sim();
        console.log("emitting", this.state.value);
        if (this.state.include_counterfactual){
          this.state.socket.emit('agent_angle',
                      {
                          'id':this.state.id,         // Pass the agent_id stored in state
                          'value':this.state.value,    // Pass the cur_angle stored in state
                          'counterfactual':  {
                                    is_pos_x: false,
                                    is_pos_z: false,
                                    is_angle: true,
                                    is_forward_step: false,
                                    is_light: false,
                                    lights: null,
                                    is_value: true,
                                    is_range: false,
                                    value: this.state.value,
                                    range: {
                                      is_gt: false,
                                      is_lt: false,
                                      is_gte: false,
                                      is_lte: false,
                                      low_bound: 0.0,
                                      high_bound: 0.0,
                                    },
                          }   // Pass the counterfactual inferred from state
                      }); // End emit
          } else{
          this.state.socket.emit('agent_angle',
                      {
                          'id':this.state.id,         // Pass the agent_id stored in state
                          'value':this.state.value,    // Pass the cur_angle stored in state
                          'counterfactual': null, 
                      }); // End emit
        }
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
            <div>
              <label>
                <input
                  type="checkbox"
                  checked={this.state.include_counterfactual}
                  onChange={value => this.include_counterfactual(value)}
                />
                Include Counterfactual
              </label>

              <p>{this.state.include_counterfactual.toString()}</p>
            </div>
      </div>

    )
    } // End Render
} // End Class

// Let us use in other componenets
export default AngleDial;
