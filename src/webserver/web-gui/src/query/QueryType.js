import React from "react";

import Select from 'react-select';

// Component to spit out agent information
class QueryType extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      query_type: 'is_pos_x',
    };

    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(type) {
    // Update our state
    this.setState({
      query_type: type,
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
    const defaultValue = { value: 'is_pos_x', label: 'x position'};

    return( 
      <div>
        <p> <br />Query Type: </p>
        <Select
          defaultValue={defaultValue}
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}

export default QueryType;
