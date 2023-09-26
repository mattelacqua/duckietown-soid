import React from "react";
import '../environment/StateButtons.css';

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
      <div class='StateButtons'>
          <button className='delete_agent' onClick={this.handleClick}> Delete </button>
      </div>
      );
    }
}


export default DeleteAgent;
