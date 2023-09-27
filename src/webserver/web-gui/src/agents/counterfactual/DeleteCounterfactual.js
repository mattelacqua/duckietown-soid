import React from "react";
import '../environment/StateButtons.css';

// Component to spit out agent information
class DeleteCounterfactual extends React.Component {

  constructor(props) {
    super(props);
    this.State = {
    };
  }

  handleClick = () => {
    console.log('deleting counterfactual ' + this.props.index);
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
      <div class='DeleteAgent'>
          <button onClick={this.handleClick}> Delete Counterfactual {this.props.index} </button>
      </div>
      );
    }
}


export default DeleteCounterfactual;
