import React from "react";
import './Buttons.css';

import Select from 'react-select';

// Component to spit out agent information
class SignalChoice extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
        agent_id: props.agent_id,
        signal_choice: props.signal_choice,
        socket: props.socket,
    };
    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(signal) {
    this.setState({
      signal_choice: signal,
    });
    this.state.socket.emit('signal_choice',
        {
            'agent_id':this.state.agent_id,
            'signal':signal,
            
        });
  }
  
  // Render the information to screen
  render() {
    const options = [
          { value: 'Right', label: 'Right' },
          { value: 'Left', label: 'Left' },
          { value: 'Straight', label: 'Straight' },
          { value: 'Random', label: 'Random' }];
    const defaultValue = { value: this.state.signal_choice, label: this.state.signal_choice}

    return( 
      <div>
        <p> Signal Choice: </p>
        <Select
          defaultValue={defaultValue}
          options={options} // Options to display in the dropdown
          onChange= {new_option => {this.handleChoice(new_option.label)}}
          />
      </div>);
  }
}


export default SignalChoice;
