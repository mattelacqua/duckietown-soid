import React from "react";
import './Buttons.css';

import Select from 'react-select';

// Component to spit out agent information
class TurnChoice extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
        agent_id: props.agent_id,
        turn_choice: props.turn_choice,
        socket: props.socket,
    };
    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(turn) {
    this.setState({
      turn_choice: turn,
    });
    this.state.socket.emit('turn_choice',
        {
            'agent_id':this.state.agent_id,
            'turn':turn,
            
        });
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: 'Right', label: 'Right' },
          { value: 'Left', label: 'Left' },
          { value: 'Straight', label: 'Straight' },
          { value: 'Random', label: 'Random' }];
    const defaultValue = { value: this.state.turn_choice, label: this.state.turn_choice}

    return( 
      <div>
        <p> <br />Turn Choice: </p>
        <Select
          defaultValue={defaultValue}
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.label)}}
          />
      </div>);
  }
}


export default TurnChoice;
