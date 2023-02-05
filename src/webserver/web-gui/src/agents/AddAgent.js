import React from "react";
import '../environment/StateButtons.css';

// Component to spit out agent information
class AddAgent extends React.Component {

  // Construct so it takes properties and they are information
  //this may not be needed
  constructor(props) {
    super(props);
    this.State = {
    };
  }

  handleClick = () => {
    this.props.socket.emit('add_agent');
  }

  // Render the information to screen
  render() {
    return (
      <div class='Buttons'>
          <button className='add_agent' onClick={this.handleClick}> Add Agent {this.props.agent.id} </button>
      </div>
      );
    }
}


export default AddAgent;
