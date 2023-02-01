import React from "react";

import Select from 'react-select';

// Component to spit out agent information
class ValueType extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      range_type: 'is_pos_x',
    };

    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(type) {
    // Update our state
    this.setState({
      range_type: type,
    });
    
    // Do the callback to set the type
    this.props.set_value_type(type);
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: 'is_value', label: 'single value' },
          { value: 'is_range', label: 'range' },
    ];

    return( 
      <div class = 'value-style'>
        <p> <br />Value Type: </p>
        <Select
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}

export default ValueType;
