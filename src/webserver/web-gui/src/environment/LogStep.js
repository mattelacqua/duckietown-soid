// Import React
import React from "react";

// Import Range
import InputRange from 'react-input-range';
import "react-input-range/lib/css/index.css";

// Component for AngleDial (rendered from Agent)
class LogStep extends React.Component {

  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    this.state = {
      step: this.props.step,
      max_step: this.props.max_step,
      socket: this.props.socket,     // Socket
    };
  }

  // Update the dial state on new changes
  handleChange = (newValue) => {
    this.state.socket.emit('log_step',
                           {
                             // the slider displays a step zero so that it looks reasonable before a run starts
                             // but not step zero actually exists -- so we need to account for this fencepost
                             'step': this.state.step - 1
                           });
    this.setState({step: newValue});
  };

  // Render the Dial component from the react-dial-knob package
  render() {
    if (this.props.max_step > this.state.max_step) {
      this.setState({
        step: this.props.step,
        max_step: this.props.max_step,
        socket: this.props.socket,     // Socket
      });
    }

    let run = (this.props.sim_state === 'run')
    let std = (this.props.started === true)

    // if we're running dial isn't useful and is confusing
    return (
      <div className="LogStep" style={{'pointer-events' : (run || !std) ? 'none' : 'auto', 'opacity' : (run || !std) ? '0.5' : '1', width : '125px'}}>
        <form className="form">
          <p>Log Step</p>
          <InputRange
            maxValue = {(this.state.max_step) ? (this.state.max_step) : 0}
            minValue = {0}
            value={this.state.step}
            step = {1}
            onChangeComplete={value => {this.handleChange(value, )}}
            onChange={value => this.setState({ step:value })}
          />
        </form>
      </div>
    )
  } // End Render
} // End Class

// Let us use in other componenets
export default LogStep;
