import React from "react";
import './StateButtons.css';

// Component to spit out agent information
class StateButtons extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {};
    this.handleClick = this.handleClick.bind(this);
  }

  // Handle the click
  async handleClick(state) {
    this.setState({
      sim_state: state,
    });

    if (state === 'pause') {
      this.props.socket.emit('update_sim_info');

      // for some reason wrapping this update_from_sim() call prevents a 'missing bracket' error -- I have no idea why...
      let self = this
      setTimeout(() => {
        // in case the user doesn't actually alter the slider we need to emit the log step
        // so that the server knows the set to query, see LogStep.js for '- 1' explanation
        self.props.update_from_sim()
          .then((env_info) => {
            self.props.socket.emit('log_step', { 'step': env_info.sim_step })
          });
      }, 1000);
    }

    this.props.socket.emit('sim_state', {'state' : state});
}

  // Render the information to screen
  render() {
    if (!this.props.started) {
      return (
        <div class='StateButtons'>
          {/* Running */}
          {this.props.sim_state === 'run' &&
           <button className='pause' onClick={()=>this.handleClick("pause")}>&nbsp;&nbsp;Pause&nbsp;&nbsp;</button>
          }

          {/* Paused */}
          {this.props.sim_state === 'pause' &&
           <button className = "start" onClick={()=>this.handleClick("run")}>&nbsp;&nbsp;&nbsp;&nbsp;Run&nbsp;&nbsp;&nbsp;&nbsp;</button>
          }
        </div>
      );
    };

    return (
      <div class='StateButtons'>
        {/* Running */}
        {this.props.sim_state === 'run' &&
          <button className='pause' onClick={()=>this.handleClick("pause")}>&nbsp;&nbsp;Pause&nbsp;&nbsp;</button>
        }

        {/* Paused */}
        {this.props.sim_state === 'pause' &&
            <button className = "resume" onClick={()=>this.handleClick("run")}>Resume</button>
        }
     </div>
    );
  }
}

export default StateButtons;
