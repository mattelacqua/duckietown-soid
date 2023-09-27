import React from "react";

import Select from 'react-select';

// Component to spit out agent information
class CounterfactualType extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      cf_type: 'is_pos_x',
    };

    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(type) {
    // Update our state
    this.setState({
      cf_type: type,
    });
    
    // Do the callback to set the type
    this.props.set_type(type);
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: 'is_pos_x', label: 'x position' },
          { value: 'is_pos_z', label: 'z position' },
          { value: 'is_angle', label: 'angle' },
          { value: 'is_forward_step', label: 'forward step (acceleration)' },
          { value: 'is_speed', label: 'Speed' },
          { value: 'is_signalchoice', label: 'Signal Choice' },
          { value: 'is_turnchoice', label: 'Turn Choice' }
    ];

    return( 
      <div>
        <p> <br />Counterfactual Type: </p>
        <Select
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}

export default CounterfactualType;