import React from "react";
import '../environment/Buttons.css';

// Component to spit out agent information
class DeleteAgent extends React.Component {

  constructor(props) {
    super(props);
    this.State = {
    };
  }

  handleClick = () => {
    console.log('deleting query ' + this.props.index);
    this.props.socket.emit('delete_counterfactual', {'index':this.props.index});
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


export default DeleteAgent;
