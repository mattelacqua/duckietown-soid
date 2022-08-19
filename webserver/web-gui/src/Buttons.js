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
    if (state !== "add_agent") {
      this.setState({
        sim_state: state,
      });
      this.props.sim_state_pass(state);
      if (state === 'pause') {
          console.log("Emiiting update_sim_info");
          socket.emit('update_sim_info');
          setTimeout(this.props.update_from_sim(), 1000);
      }
      console.log("Emiiting sim_state");
      socket.emit('sim_state',
                  {
                      'state':state,
      });
    } else {
        socket.emit('add_agent');
    }

  }
  
  // Render the information to screen
  render() {
    return (
      <div class='Buttons'>

          {this.props.sim_state === 'run' &&
            <button className='pause' onClick={()=>this.handleClick("pause")}>Pause</button>
          }
          {this.props.sim_state === 'run' &&
            <button className='quit' onClick={()=>this.handleClick("quit")}>Quit</button>
          }
         {this.props.sim_state === 'pause' &&
            <button className='add_agent' onClick={()=>this.handleClick("add_agent")}>Add New Agent</button>
         }
         {this.props.sim_state === 'pause' &&
            <button className = "resume" onClick={()=>this.handleClick("run")}>Resume</button>
         }
         {this.props.sim_state === 'pause' &&
            <button className='quit' onClick={()=>this.handleClick("quit")}>Quit</button>
         }
      </div>
      );
    }
}


export default Buttons;
