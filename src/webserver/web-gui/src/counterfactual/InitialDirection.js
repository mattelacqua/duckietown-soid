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
    
    // Do the callback to set the type
    this.props.set_initial_direction(direction);
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: 'N', label: 'N' },
          { value: 'S', label: 'S' },
          { value: 'E', label: 'E' },
          { value: 'W', label: 'W' },
    ];

    return( 
      <div>
        <p> <br />Initial Direction: </p>
        <Select
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}

export default InitialDirection;
