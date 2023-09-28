import React from "react";

import Select from 'react-select';

// Component to spit out agent information
class SingleDirection extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      selection: 'Right',
    };

    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(direction) {
    // Update our state
    this.setState({
      selection: direction,
    });
    
    // Do the callback to set the type
    console.log('direction', direction);
    this.props.set_single_direction(direction, this.props.signal_or_turn);
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: 'Left', label: 'Left' },
          { value: 'Right', label: 'Right' },
          { value: 'Straight', label: 'Straight' },
    ];

    const default_val = this.props.direction;
    return( 
      <div>
        of
        <Select
          defaultValue={default_val}
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}


export default SingleDirection;
