import React from "react";
import './Buttons.css';

import io from 'socket.io-client';

const socket = io();

// Component to spit out agent information
class DeleteAgent extends React.Component {

  // Construct so it takes properties and they are information
  //this may not be needed
  constructor(props) {
    super(props);
  }

  handleClick = () => {
    console.log('deleting agent ' + this.props.agent_id);
    socket.emit('delete_agent', {'id':this.props.agent_id});
  }


  
  // Render the information to screen
  render() {
    return (
      <div class='DeleteAgent'>
          <button onClick={this.handleClick}>X</button>
      </div>
      );
    }
}


export default DeleteAgent;
