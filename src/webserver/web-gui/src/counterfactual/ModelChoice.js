import React from "react";

import Select from 'react-select';

// Component to spit out agent information
class ModelChoice extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      model: 'good_agent',
    };
    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(choice) {
    // Update our state
    this.setState({
      model: choice,
    });
    
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: 'good_agent', label: 'Good Agent (Hard-Coded Behavior)' },
          { value: 'defensive', label: 'Defensive (Learned)' },
          { value: 'standard', label: 'Standard (Learned)' },
          { value: 'reckless', label: 'Reckless (Learned)' },
          { value: 'pathological', label: 'Pathological (Learned)' }
    ];

    return( 
      <div>
        <p> <br />Agent 0's Decision Model: </p>
        <Select
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}

export default ModelChoice;
