import React from "react";
import '../../environment/StateButtons.css';

// Component to spit out agent information
class DeleteCounterfactual extends React.Component {

  constructor(props) {
    super(props);
    this.state = {};
  }

  handleClick = () => {
    this.props.socket.emit(
      'delete_counterfactual', 
      {
        'index':this.props.index,
        'agent_index': this.props.agent_index,
      });
  }

  // Render the information to screen
  render() {
    return (
      <div class='StateButtons'>
          <button className='delcounterfac' onClick={this.handleClick}> Delete </button>
      </div>
      );
    }
}


export default DeleteCounterfactual;
