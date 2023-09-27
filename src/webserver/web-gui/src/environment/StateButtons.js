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
      started: true,
    });

    if (state === 'pause') {
      this.props.socket.emit('update_sim_info');

      // for some reason wrapping this update_from_sim() call prevents a 'missing bracket' error -- I have no idea why...
      let self = this
      setTimeout(() => { self.props.update_from_sim() }, 1000);
    }
    this.props.socket.emit('sim_state', {'state' : state});
}

  // Render the information to screen
  render() {
    if (!this.props.started) {
      return (
        <div class='StateButtons'>
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
