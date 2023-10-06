import React from 'react'


class CounterfactualModel extends React.Component {

  constructor(props) {
    super(props);
    this.state = {};
  }

  // Render the conponents
  render() {
    
    let nmap = {
      'is_angle' : 'angle',
      'is_forward_step' : 'forward_step',
      'is_pos_x' : 'pos_x',
      'is_pos_z' : 'pos_z',
      'is_range' : 'range',
      'is_signalchoice' : 'signal_choice',
      'is_speed': 'speed',
      'is_turnchoice' : 'turn_choice'
    }

    let value  = 'N/A';
    let format = false;
    if (this.props.model) {
      [ 'is_angle', 'is_forward_step', 'is_pos_x', 'is_pos_z',  'is_range', 'is_signalchoice', 'is_speed', 'is_turnchoice' ].forEach((type) => {
        if (this.props.counterfactual[type]) {
          if (type === 'is_signalchoice' || type === 'is_turnchoice') format = true;
          value = this.props.model[nmap[type]];
        }
      });
    }
    
    return (
      <div className="Model">
        {(format)
         ? <p><b><i>{(!this.props.finished) ? '???' : value.toString().toLowerCase()}</i></b></p>
         : <p><b>{(!this.props.finished) ? '???' : value}</b></p> }
      </div>
    )
  }
}

export default CounterfactualModel;
