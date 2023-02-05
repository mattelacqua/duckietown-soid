import React from "react";
import './StateButtons.css';


// Component to spit out agent information
class StateButtons extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
        sim_state: this.props.sim_state,
        socket: this.props.socket
    };
    this.handleClick = this.handleClick.bind(this);
  }
  
  // Handle the click
  async handleClick(state) {
    this.setState({
      sim_state: state,
    });

    if (state === 'pause') {
        this.props.socket.emit('update_sim_info');
        setTimeout(this.props.update_from_sim(), 1000);
    }
    this.props.socket.emit('sim_state', {'state':state});
}
  
  // Render the information to screen
  render() {
    return (
      <div class='StateButtons'>

        {/* Running */}
        {this.props.sim_state === 'run' &&
          <button className='pause' onClick={()=>this.handleClick("pause")}>Pause</button>
        }
        {this.props.sim_state === 'run' &&
          <button className='quit' onClick={()=>this.handleClick("quit")}>Quit</button>
        }

        {/* Paused */}
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

export default StateButtons;