// Import React
import React from "react";

import Select from 'react-select';

// Agent Component (gets rendered in app)
class IntersectionArrival extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      value: props.agent.intersection_arrival,
      step:  props.sim_step,
    };

    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(arrival) {
    // Update our state
    this.setState({
      intersection_arrival: arrival,
    });
    
    // Send the new direction to socket
    this.props.socket.emit(
      'intersection_arrival', 
      {
       agent_index: this.props.agent.id,
       intersection_arrival: arrival,
      });
  }

  // Render the agent component 
  render() {
    const options = [];

    for (let i = 0; i < this.state.step; i++) options.push({ value: i.toString(), label: i.toString() });

    let active = (this.state.value >= 0);

    return( 
      <div className='IntersectionArrival' style={{'pointer-events' : (!active) ? 'none' : 'auto', 'opacity' : (!active) ? '0.5' : '1'}}>
        <h4> Time of Intersection Arrival: </h4>
        <Select
          options={options} // Options to display in the dropdown
          defaultValue={{value: this.state.value.toString(), label: (active) ? this.state.value.toString() : "N/A"}}
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

// Allow it to be called in other functions
export default IntersectionArrival;
