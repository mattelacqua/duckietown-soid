import React from "react";
import './Buttons.css';

import io from 'socket.io-client';

const socket = io();

// Component to spit out agent information
class Buttons extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
        sim_state: this.props.sim_state
    };
    this.handleClick = this.handleClick.bind(this);
  }

  // Handle the click
  handleClick(state) {
    this.setState({
      sim_state: state,
    });
    this.props.sim_state_pass(state);
    if (state === 'pause') {
        socket.emit('update_sim_info');
        setTimeout(this.props.update_from_sim(), 1000);
    }
    socket.emit('sim_state',
                {
                    'state':state,
                });

  }
  
  // Render the information to screen
  render() {
    return (
      <div class='Buttons'>

          <button className = "resume" onClick={()=>this.handleClick("run")}>Resume</button>
          <button className='pause' onClick={()=>this.handleClick("pause")}>Pause</button>
          <button className='quit' onClick={()=>this.handleClick("quit")}>Quit</button>

      </div>
      );
    }
}


export default Buttons;
