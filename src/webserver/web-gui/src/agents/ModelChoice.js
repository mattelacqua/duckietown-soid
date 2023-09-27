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

    this.props.socket.emit(
      "model_choice",
      {
        'choice': choice,
      }
    );
    
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
      <div className="ModelChoice">
        <h4> Decision Model: </h4>
        <Select
          options={options} // Options to display in the dropdown
          defaultValue={{value: 'good_agent', label: 'Good Agent (Hard-Coded Behavior)'}} // Options to display in the dropdown
          theme={theme => ({
            ...theme,
            borderRadius: 0,
            colors: {
              ...theme.colors,
              primary25: '#DDCC77',
              primary: '#999933',
            },
          })}
          onChange= {new_option => {this.handleChoice(new_option.value)}}
          />
      </div>);
  }
}

export default ModelChoice;
