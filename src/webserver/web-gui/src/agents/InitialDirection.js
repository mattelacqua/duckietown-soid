import React from "react";

import Select from 'react-select';

// Component to spit out agent information
class InitialDirection extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      initial_direction: 'N',
    };

    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(direction) {
    // Update our state
    this.setState({
      initial_direction: direction,
    });
    
    // Send the new direction to socket
    this.props.socket.emit(
      'initial_direction', 
      {
       agent_index: this.props.agent.id,
       initial_direction: direction,
      });
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: '0', label: 'N' },
          { value: '1', label: 'S' },
          { value: '2', label: 'E' },
          { value: '3', label: 'W' },
    ];

    return( 
      <div>
        <p> <br />Initial Direction: </p>
        <Select
          options={options} // Options to display in the dropdown
          defaultValue={this.props.agent.initial_direction}
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}

export default InitialDirection;
