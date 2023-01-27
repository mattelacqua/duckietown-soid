import React from "react";

import Select from 'react-select';

// Component to spit out agent information
class Operator extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      selection: '>',
    };

    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(operator) {
    // Update our state
    this.setState({
      selection: operator,
    });
    
    // Do the callback to set the type
    this.props.set_operator(operator);
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: '>', label: '>' },
          { value: '<', label: '<' },
          { value: '>=', label: '>=' },
          { value: '<=', label: '<=' },
    ];

    return( 
      <div>
        <p> <br /> Operator : </p>
        <Select
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}


export default Operator;
