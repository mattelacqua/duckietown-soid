import React from "react";
import './Buttons.css';

// Component to spit out agent information
class DeleteAgent extends React.Component {

  // Construct so it takes properties and they are information
  //this may not be needed
  constructor(props) {
    super(props);
    this.State = {
      socket: props.socket,
    };
  }

  handleClick = () => {
    console.log('deleting agent ' + this.props.agent_id);
    this.props.socket.emit('delete_agent', {'id':this.props.agent_id});
  }

  // Render the information to screen
  render() {
    return (
      <div class='DeleteAgent'>
          <button onClick={this.handleClick}> Delete Agent {this.props.agent_id} </button>
      </div>
      );
    }
}


export default DeleteAgent;
