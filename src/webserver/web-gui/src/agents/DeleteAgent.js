import React from "react";
import '../environment/Buttons.css';

// Component to spit out agent information
class DeleteAgent extends React.Component {

  // Construct so it takes properties and they are information
  //this may not be needed
  constructor(props) {
    super(props);
    this.State = {
    };
  }

  handleClick = () => {
    this.props.socket.emit('delete_agent', {'id':this.props.agent.id});
  }

  // Render the information to screen
  render() {
    return (
      <div class='Buttons'>
          <button className='delete_agent' onClick={this.handleClick}> Delete Agent {this.props.agent.id} </button>
      </div>
      );
    }
}


export default DeleteAgent;
